"""Маршруты генетического профиля пациента."""

import json
from pathlib import Path

from fastapi import APIRouter, Depends, FastAPI, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from src.schemas.gene_analysis import GeneAnalysisReport, ProfileResponse
from src.services.gene_analysis.errors import GeneAnalysisError
from src.services.gene_analysis.profile_storage import ProfileStorage
from src.services.gene_analysis.service import analyze_profile
from .dependencies import get_profile_storage, locked_patient, require_patient

router = APIRouter(prefix="/genes", tags=["Генетический профиль"])
EXAMPLES_DIR = Path(__file__).resolve().parents[2] / "schemas" / "gene_analysis" / "examples"
REPORT_EXAMPLES = {
    name: {"summary": label, "value": json.loads((EXAMPLES_DIR / f"{name}.json").read_text(encoding="utf-8"))}
    for name, label in (("complete", "Полный синтетический отчёт"), ("partial", "ClinVar временно недоступен"))
}


def install_report_examples(app: FastAPI) -> None:
    """Сохраняет null в примерах: стандартный генератор FastAPI удаляет их рекурсивно."""
    generate_openapi = app.openapi

    def openapi() -> dict:
        schema = generate_openapi()
        operation = schema["paths"]["/api/patients/{patient_id}/genes/analysis"]["get"]
        operation["responses"]["200"]["content"]["application/json"]["examples"] = REPORT_EXAMPLES
        return schema

    app.openapi = openapi


@router.get("/profile", response_model=ProfileResponse, summary="Получить текущий профиль",
            dependencies=[Depends(require_patient)])
async def get_profile(patient_id: int, storage: ProfileStorage = Depends(get_profile_storage)) -> ProfileResponse:
    try:
        profile = await run_in_threadpool(storage.current, patient_id)
    except GeneAnalysisError as exc:
        raise HTTPException(exc.status_code, str(exc)) from exc
    return ProfileResponse(profile=profile)


@router.post("/profile", response_model=ProfileResponse, summary="Загрузить или заменить VCF")
async def upload_profile(patient_id: int, file: UploadFile = File(...),
                         storage: ProfileStorage = Depends(locked_patient)) -> ProfileResponse:
    """Устанавливает новый профиль после проверки; прежний отчёт удаляется."""
    try:
        profile = await run_in_threadpool(storage.replace, patient_id, file.filename or "", file.file)
        return ProfileResponse(profile=profile)
    finally:
        await file.close()


@router.get("/analysis", response_model=GeneAnalysisReport, summary="Получить анализ генетического профиля",
            responses={200: {"content": {"application/json": {"examples": REPORT_EXAMPLES}}}})
async def get_analysis(patient_id: int, storage: ProfileStorage = Depends(locked_patient)) -> GeneAnalysisReport:
    """Первый запрос ожидает расчёт; последующие возвращают сохранённый снимок, включая частичный."""
    return await run_in_threadpool(analyze_profile, patient_id, storage)
