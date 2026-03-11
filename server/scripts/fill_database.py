"""
Fills the database with dummy data for patient id=1 (Иван Петров, 40).
Run from the server root: python scripts/fill_database.py
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models.patient import Patient
from src.models.health_indicators import (
    GeneralInfo,
    LaboratoryInfo,
    AllergiesInfo,
    FamilyHistoryInfo,
    VaccinationsInfo,
    LifestyleInfo,
)
from src.models.medical_documents import (
    DiseasesHistoryDoc,
    DiseasesHistoryDocDetails,
    AnalyzesDoc,
    RecommendationsDoc,
    OtherDoc,
)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "persomed.db")
engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}")
session_maker = async_sessionmaker(engine, expire_on_commit=False)

PATIENT_ID = 1


def _target_reached(value, min_val, max_val) -> bool | None:
    if min_val is None or max_val is None:
        return None
    try:
        return min_val <= float(value) <= max_val
    except (ValueError, TypeError):
        return None


async def insert_patient(session) -> None:
    patient = Patient(id=PATIENT_ID, name="Иван", surname="Петров", age=40)
    session.add(patient)
    await session.commit()
    print("Created patient: Иван Петров, 40")


async def insert_general_info(session, items: list) -> None:
    for item in items:
        min_v = item.get("targetLevelMin")
        max_v = item.get("targetLevelMax")
        obj = GeneralInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=item.get("value", ""),
            unit=item.get("unit"),
            date=item.get("date"),
            target_level_min=min_v,
            target_level_max=max_v,
            target_reached=_target_reached(item.get("value", ""), min_v, max_v),
        )
        session.add(obj)
    await session.commit()
    print(f"Added {len(items)} general health indicators")


async def insert_laboratory_info(session, items: list) -> None:
    for item in items:
        min_v = item.get("targetLevelMin")
        max_v = item.get("targetLevelMax")
        try:
            value = float(item.get("value", 0))
        except (ValueError, TypeError):
            print(f"  [skip] invalid float value for: {item.get('name')}")
            continue
        obj = LaboratoryInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=value,
            unit=item.get("unit"),
            date=item.get("date"),
            target_level_min=min_v,
            target_level_max=max_v,
            target_reached=_target_reached(value, min_v, max_v),
        )
        session.add(obj)
    await session.commit()
    print(f"Added {len(items)} laboratory indicators")


async def insert_allergies_info(session, items: list) -> None:
    for item in items:
        session.add(AllergiesInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=item.get("value", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} allergy records")


async def insert_family_history_info(session, items: list) -> None:
    for item in items:
        session.add(FamilyHistoryInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=item.get("value", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} family history records")


async def insert_vaccinations_info(session, items: list) -> None:
    for item in items:
        session.add(VaccinationsInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=item.get("value", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} vaccination/preventive records")


async def insert_lifestyle_info(session, items: list) -> None:
    for item in items:
        session.add(LifestyleInfo(
            patient_id=PATIENT_ID,
            name=item["name"],
            canonical_name=item.get("canonicalName"),
            value=item.get("value", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} lifestyle records")


async def insert_diseases_history_docs(session, items: list) -> None:
    for item in items:
        session.add(DiseasesHistoryDoc(
            patient_id=PATIENT_ID,
            name=item["name"],
            type=item["type"],
            date=item["date"],
            icd_code=item.get("icdCode", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} disease history documents")


async def insert_analyzes_docs(session, items: list) -> None:
    for item in items:
        session.add(AnalyzesDoc(
            patient_id=PATIENT_ID,
            name=item["name"],
            type=item["type"],
            date=item["date"],
        ))
    await session.commit()
    print(f"Added {len(items)} analysis documents")


async def insert_recommendations_docs(session, items: list) -> None:
    for item in items:
        session.add(RecommendationsDoc(
            patient_id=PATIENT_ID,
            name=item["name"],
            type=item["type"],
            date=item["date"],
            specialty=item.get("specialty", ""),
        ))
    await session.commit()
    print(f"Added {len(items)} recommendation documents")


async def insert_other_docs(session, items: list) -> None:
    for item in items:
        session.add(OtherDoc(
            patient_id=PATIENT_ID,
            name=item["name"],
            type=item["type"],
            date=item["date"],
        ))
    await session.commit()
    print(f"Added {len(items)} other documents")


async def insert_document_details(session, details: dict, diseases_history: list) -> None:
    """Insert DiseasesHistoryDocDetails from document_details section."""
    for key, detail in details.items():
        doc_id = int(detail["documentId"])
        meta = detail["meta"]
        sections = detail["sections"]
        obj = DiseasesHistoryDocDetails(
            id=doc_id,
            document_id=doc_id,
            title=detail.get("title", ""),
            icd_code=meta.get("icdCode", ""),
            diagnosis_date=meta.get("diagnosisDate", ""),
            doctor=meta.get("doctor", ""),
            specialty=meta.get("specialty", ""),
            nosology=meta.get("nosology", ""),
            disease_type=meta.get("diseaseType", ""),
            clinic_name=meta.get("clinicName", ""),
            anamnesis=sections.get("anamnesis", ""),
            clinical_findings=sections.get("clinicalFindings"),
            diagnosis=sections.get("diagnosis"),
            treatment_plan=sections.get("treatmentPlan"),
            conclusion=sections.get("conclusion"),
        )
        session.add(obj)
    await session.commit()
    print(f"Added {len(details)} document detail records")


async def fill_database() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "dummy.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    async with session_maker() as session:
        await insert_patient(session)
        await insert_general_info(session, data["general"])
        await insert_laboratory_info(session, data["detailed"])
        await insert_allergies_info(session, data["allergies"])
        await insert_family_history_info(session, data["family_history"])
        await insert_vaccinations_info(session, data["preventive"])
        await insert_lifestyle_info(session, data["lifestyle"])
        await insert_diseases_history_docs(session, data["diseases_history"])
        await insert_analyzes_docs(session, data["analyzes"])
        await insert_recommendations_docs(session, data["recommendations"])
        await insert_other_docs(session, data["other_docs"])
        await insert_document_details(session, data.get("document_details", {}), data["diseases_history"])

    print("\nDatabase filled successfully!")


if __name__ == "__main__":
    asyncio.run(fill_database())
