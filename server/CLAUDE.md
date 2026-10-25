# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PersoMed server: a FastAPI backend for a personalized medical information system. It stores a patient's digital profile (health indicators, medical documents) and runs NLP/ML analysis on it (symptom extraction, disease prediction, risk factors, drug recommendations). User-facing strings, API tags, docstrings and most comments are in **Russian**; keep new user-facing text in Russian.

There is no test suite, linter config or CI. You can check changes by running the server and calling the endpoints through Swagger at `http://localhost:8000/docs`.

## Commands

Python is pinned to **3.11.8** (`.python-version`). The local virtualenv is `venv/`. `venv-pyctd/` is a separate env used only by the pyctd experiments.

```bash
# Dev server (VS Code "Launch Debug" config does the same with PYTHONPATH=workspace root)
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Docker: the container's CMD serves on port 80, not 8000
docker build -t persomed-server .
docker run -p 80:80 persomed-server

# Migrations (alembic.ini points at sqlite+aiosqlite:///persomed.db, relative to CWD)
alembic upgrade head
alembic revision --autogenerate -m "description"
alembic downgrade -1

# Seed patient id=1 (Иван Петров) from scripts/dummy.json
python scripts/fill_database.py

# Genetic profile analysis (standalone; defaults to genetical_profile_short.vcf)
python scripts/genes_analysis/analysis.py [path/to/file.vcf]
python scripts/genes_analysis/check_pgs_candidates.py
```

Run everything from the server root: the SQLite path `persomed.db` and the `src.` imports are resolved relative to the current working directory.

`requirements.txt` lists only direct dependencies, for both the server and `scripts/genes_analysis`, pinned to versions known to work. `medcat 1.15.2` constrains `numpy<1.26` and `scipy~=1.9.2`, so don't bump numpy or scipy without upgrading medcat. Run `pip check` after changing dependencies.

## Architecture

Async SQLAlchemy 2.0 over SQLite (`aiosqlite`), Pydantic v2 schemas, and a strict layering:

```
src/api/          FastAPI routers (one module per domain, sub-routers per subtype)
src/schemas/      Pydantic request (…Create/…Update) and response models
src/repositories/ Data access; all extend BaseRepository[T]
src/models/       SQLAlchemy ORM models (all registered in src/models/__init__.py)
src/services/     Analysis logic: NLP, ML, ontology, translation, aggregation
src/database.py   Engine, session maker, Base; enables PRAGMA foreign_keys=ON on connect
src/db_depends.py get_async_db() dependency used by every DB-backed route
```

Routes instantiate repositories directly: `repository = XRepository(db)`. There is no service layer for CRUD. `BaseRepository` provides `get_all`, `get_all_by_patient`, `get_by_id`, `create`, `update` and `delete`, and **each of these commits immediately**.

### URL layout (`src/api/__init__.py`)

Everything is under `/api`. Patient-scoped routers are mounted under `/api/patients/{patient_id}`:

| Path | Purpose |
|---|---|
| `/api/patients` | Patient CRUD |
| `/api/patients/{id}/health-indicators/{general,laboratory,vaccinations,allergies,family-history,lifestyle}` | Indicator CRUD |
| `/api/patients/{id}/medical-documents/{analyzes,diseases-history,recommendations,other}` | Document CRUD (+ `/{document_id}/details` for diseases-history and recommendations) |
| `/api/patients/{id}/risk-analysis/risk-factors` | Abnormal indicators + chronic diseases |
| `/api/patients/{id}/patient-status/` | Aggregated dashboard (see below) |
| `/api/diagnostic/diseases` | POST symptoms → ML + ontology disease predictions |
| `/api/recommendations/drugs` | POST disease → drugs from the ontology |
| `/api/text-processing/extract-entities` | MedCAT NER on free text |

Patient-scoped routes receive `patient_id` from the path. They must inject it on create (`{**data.model_dump(), "patient_id": patient_id}`) and return 404 when `item.patient_id != patient_id`. Follow that pattern in new patient-scoped routes. The `/details` sub-routes currently skip the patient ownership check.

### Data model conventions

- `HealthIndicatorBase` / `MedicalDocumentBase` are abstract models that hold `id`, `patient_id` (FK → `patients.id`, `ondelete=CASCADE`), and shared fields. Dates are stored as **strings**, not date types.
- `HealthIndicatorRepository` computes `target_reached` on create and update from `value` against `target_level_min/max`. `value` is a string and is cast to float.
- `DiseasesHistoryDocDetails` and `RecommendationsDocDetails` are one-to-one with their document, and their **primary key `id` equals `document_id`** (both are FKs to the parent). The API sets both explicitly when it creates details. The details request schemas are nested (`meta`, `sections`), and the routes flatten them into columns by hand.
- When you add or change a model, import it in `src/models/__init__.py` (Alembic's `env.py` imports `src.models` to collect metadata). Then autogenerate a migration. `render_as_batch=True` is set for SQLite ALTER support.

### Services

- **Translation** (`services/translate`): the whole NLP/ML stack works in English. Russian input goes through `translate_to_english`, and results come back through `translate_to_russian`. Translation uses a small medical dictionary first, then falls back to `GoogleTranslator` from deep-translator, which needs network access and returns the original text if it fails. On the way out, text is lowercased (to English) or capitalized (to Russian).
- **Text processing** (`services/text_processing`): `TextProcessingService` is a singleton that loads a MedCAT UMLS model pack from `src/services/text_processing/models/umls_small_model` (directory or `.zip`). That model is **gitignored and must be obtained separately**, and the first call is slow. Entities include `type_ids` (UMLS TUIs). The code filters on `T184` = symptom, and on `T200`/`T121` = drug.
- **Diagnostic** (`services/diagnostic`): `ml_disease_prediction` is a pickled MultinomialNB (`prediction_model.sav`) over a one-hot symptom vector built from the columns of `disease_symptoms.xlsx`, and it returns the top 3. `ontology_diseases_prediction` runs SPARQL over `services/ontology/diseases.owl` with owlready2. Symptom names must match the dataset/ontology English names exactly. Both engines reload the model/ontology **on every call**, and `get_model_info()` re-scores the whole dataset per call. `get_predictions()` in `services/diagnostic/__init__.py` wraps the full RU→EN→predict→RU flow.
- **Drug recommendations** (`services/recommendation`): SPARQL on the same ontology, using `treated_with` and falling back to `treats`.
- **Risk analysis / patient status**: these depend on **Russian document `type` values**. `"Анамнез"` marks diseases-history docs whose `anamnesis` is mined for symptoms. `"хроническое"` (case-insensitive) marks chronic disease. `"Назначения"` marks recommendation docs mined for drugs, and `"Рекомендации"` marks docs whose `instructions` are split on commas. `get_rates()` returns **hardcoded placeholder** risk ratings.
- The service "info" strings hardcode some counts ("135 заболеваний", "112 лекарственных препаратов") even though the code computes the real counts.

### Genetics (`scripts/genes_analysis/`, experimental, not wired into the API)

`analysis.py` is a 6-stage CLI pipeline:

1. Parse a VCF (PyVCF3).
2. Annotate the rsIDs through MyVariant.info (ClinVar, GWAS, CADD; hg19).
3. Filter clinically significant ClinVar records.
4. Evaluate declarative SNP/haplotype rules from `complex_genotypes.yaml`, e.g. APOE ε2/ε3/ε4 and Factor V Leiden. Add new rules there, with `sources`, instead of in Python.
5. Compute polygenic scores from PGS Catalog harmonized GRCh37 scoring files, cached in `.pgs_cache/`. Missing SNPs use EAF mean imputation, then z-score → percentile. Only scores whose scoring file has `allelefrequency_effect` give percentiles. Use `check_pgs_candidates.py` to vet PGS IDs before adding them to `DEFAULT_PGS_SCORES`.
6. Print a console report.

`genetical_profile_full.vcf` and `.pgs_cache/` are gitignored.

`scripts/pyctd/` holds experiments against the Comparative Toxicogenomics Database. They use the `pyctd.db` file in the server root, which is about 15 GB and gitignored.

## Adding a new domain

Create matching modules in `api/`, `schemas/`, `models/` and `repositories/`, export them from each package's `__init__.py`, and register the router in `src/api/__init__.py`. Mount it on `patient_info_router` if it is patient-scoped. Then add an Alembic migration.

## Code style (from `.cursor/rules/server-dev-rules.mdc`)

Type-hint function signatures, use `async def` for I/O, use Pydantic models rather than raw dicts for request validation, use guard clauses and early returns, use `HTTPException` for expected errors, and use lowercase_underscore file names. Prefer lifespan handlers over `on_event`.
