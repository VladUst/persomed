# Repository Guidelines

## Project Structure & Module Organization

This directory contains PersoMed's FastAPI backend; the frontend lives in `../client`.

- `src/main.py`: application entry point; `src/api/`: routers mounted under `/api`.
- `src/schemas/`: Pydantic request/response models; `src/models/`: SQLAlchemy models; `src/repositories/`: database access.
- `src/services/`: NLP, prediction, ontology, translation, and patient analysis. Model/data assets live alongside their services.
- `migrations/`: Alembic revisions.
- `scripts/genes_analysis/`: standalone VCF analysis and declarative rules in `complex_genotypes.yaml`; `scripts/pyctd/`: separate experiments.

Read `README.md` for setup and `CLAUDE.md` for detailed architecture.

Detailed reference documentation is available in `.claude/docs/`. Consult the relevant file before changing these areas:

- [Architecture](.claude/docs/architecture.md): application structure and component interactions.
- [API routes](.claude/docs/api.md): endpoints and request/response behavior.
- [Database](.claude/docs/database.md): data models, relationships, and migrations.

## Build, Test, and Development Commands

Use Python **3.11.8** and run commands from this directory; SQLite paths are relative to it.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

These commands create an environment, install dependencies, apply migrations, and start development serving.

- `docker build -t persomed-server .` and `docker run -p 80:80 persomed-server`: build and serve the container.
- `alembic revision --autogenerate -m "description"`: generate a migration; review it before applying.
- `python scripts/genes_analysis/analysis.py path/to/file.vcf`: run genetic analysis.
- `pip check`: validate dependency compatibility after dependency changes.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` modules/functions, `PascalCase` classes, and typed function signatures. Use Pydantic validation, asynchronous database operations, guard clauses, and `HTTPException` for expected API errors. Keep user-facing strings in Russian. No formatter or linter is configured.

Register new ORM models in `src/models/__init__.py` and routers in `src/api/__init__.py`; include migrations for schema changes.

## Testing Guidelines

Genetic-analysis tests live in `tests/` and use `python -m unittest discover -s tests -v`; install `requirements-test.txt` first. They use synthetic VCFs, temporary storage/SQLite and mocked network calls. No coverage threshold or CI exists. `scripts/pyctd/test.py` is an exploratory script. Verify other affected endpoints through `http://localhost:8000/docs`, covering success, invalid input, missing records, and patient ownership. Record reproduction commands and expected responses in the PR. Add tests as `tests/test_<feature>.py`.

## Commit & Pull Request Guidelines

Follow existing prefixes: `feat:`, `fix:`, `refactor:`, and `docs:` with concise descriptions. Keep commits focused. PRs should describe behavior changes, link relevant issues, report validation, and explain migration or dependency impacts.

## Configuration & Data

Keep patient data, full VCFs, local databases, downloaded models, and caches out of commits. Obtain the ignored MedCAT UMLS model separately. Preserve MedCAT-compatible dependency constraints.
