# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the server (development):**
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

**Run via Docker:**
```bash
docker build -t persomed-server .
docker run -p 80:8000 persomed-server
```

**Database migrations:**
```bash
alembic upgrade head          # Apply all migrations
alembic revision --autogenerate -m "description"  # Generate new migration
alembic downgrade -1          # Rollback one migration
```

**Populate DB with dummy data:**
```bash
python scripts/fill_database.py
```

Python version is pinned to **3.11.8** (see `.python-version`).

## Architecture

The app is a FastAPI-based medical information system (PersoMed) using **async SQLAlchemy with SQLite** (`persomed.db`). It follows a strict 4-layer pattern:

```
API (src/api/)  →  Repository (src/repositories/)  →  Model (src/models/)  →  DB
                        ↑
              Schema (src/schemas/) — Pydantic validation
              Service (src/services/) — Business logic (NLP/ML)
```

**Layers:**
- `src/api/` — FastAPI route handlers; each domain module has its own router
- `src/schemas/` — Pydantic models split into request (Create/Update) and response types
- `src/repositories/` — Data access; all extend `BaseRepository[T]` which provides `get_all`, `get_all_by_patient`, `get_by_id`, `create`, `update`, `delete`
- `src/models/` — SQLAlchemy ORM models; all patient-linked models have `patient_id` FK with CASCADE delete
- `src/services/` — Stateful/ML services (MedCAT NER, disease prediction, risk analysis, drug recommendations, translation)
- `src/database.py` — Async engine + session factory; SQLite foreign keys are explicitly enabled via `PRAGMA foreign_keys = ON`
- `src/db_depends.py` — FastAPI `Depends()` provider for async DB sessions

**Domain modules** (each spans all layers):
- `patients` — Core patient entity
- `health_indicators` — Six subtypes: general, laboratory, vaccination, allergy, family_history, lifestyle
- `medical_documents` — Four subtypes: analyzes, diseases_history, recommendations, other
- `diagnostic` — ML + ontology-based disease prediction from symptoms
- `risk_analysis` — Abnormal indicator detection and chronic disease risk
- `recommendations` — Drug/treatment recommendations
- `patient_status` — Aggregated patient health overview
- `text_processing` — MedCAT NER for extracting medical entities from free text

**Services of note:**
- `TextProcessingService` is a singleton (initialized once on first use) wrapping a MedCAT model for UMLS concept extraction
- `diagnostic/` has two prediction engines: ML-based (scikit-learn) and ontology-based (owlready2)
- `translate/` provides bidirectional English↔Russian translation via deep-translator
- `ontology/` manages a disease ontology used by the diagnostic service

**Adding a new domain:** create matching files in `api/`, `schemas/`, `models/`, `repositories/`; register the router in `src/api/__init__.py`.
