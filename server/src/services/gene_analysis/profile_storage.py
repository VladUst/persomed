"""Атомарные поколения профиля и отчёта под межпроцессной блокировкой."""

import hashlib
import json
import os
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterator
from uuid import uuid4

from filelock import FileLock, Timeout
from pydantic import ValidationError

from src.schemas.gene_analysis import GeneAnalysisReport, Profile
from .config import DATA_DIR, MAX_PROFILE_BYTES
from .errors import GeneAnalysisError
from .vcf_parser import parse_vcf

def atomic_json(path: Path, value: dict) -> None:
    """Записывает полный JSON перед заменой видимого файла."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as target:
            json.dump(value, target, ensure_ascii=False, allow_nan=False)
            target.flush()
            os.fsync(target.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


class ProfileStorage:
    def __init__(self, root: Path = DATA_DIR, max_bytes: int = MAX_PROFILE_BYTES):
        self.root = root.resolve()
        self.max_bytes = max_bytes

    def patient_dir(self, patient_id: int) -> Path:
        if patient_id < 1:
            raise GeneAnalysisError("Некорректный идентификатор пациента.")
        return self.root / "patients" / str(patient_id)

    @contextmanager
    def lock(self, patient_id: int) -> Iterator[None]:
        """Не ждёт другую операцию и работает между процессами Uvicorn."""
        self.patient_dir(patient_id)
        directory = self.root / "locks"
        directory.mkdir(parents=True, exist_ok=True)
        lock = FileLock(directory / f"{patient_id}.lock", timeout=0)
        try:
            lock.acquire()
        except Timeout as exc:
            raise GeneAnalysisError("Другая операция с профилем ещё выполняется.", 409) from exc
        try:
            yield
        finally:
            lock.release()

    def current(self, patient_id: int) -> Profile | None:
        """Указатель содержит метаданные целиком: чтение не зависит от очистки старого поколения."""
        path = self.patient_dir(patient_id) / "current.json"
        try:
            return Profile.model_validate_json(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except (ValueError, UnicodeError) as exc:
            raise GeneAnalysisError("Метаданные профиля повреждены; загрузите VCF повторно.", 409) from exc

    def profile_dir(self, patient_id: int, profile: Profile) -> Path:
        return self.patient_dir(patient_id) / str(profile.id)

    def replace(self, patient_id: int, filename: str, stream: BinaryIO) -> Profile:
        """Вызывается под lock; прежнее поколение остаётся доступным до полной проверки."""
        filename = filename.replace("\\", "/").rsplit("/", 1)[-1]
        if not filename.lower().endswith(".vcf") or any(ord(char) < 32 for char in filename):
            raise GeneAnalysisError("Загрузите обычный файл .vcf без сжатия.")
        patient_dir = self.patient_dir(patient_id)
        generation = uuid4()
        directory = patient_dir / str(generation)
        directory.mkdir(parents=True)
        installed = False
        try:
            size = 0
            digest = hashlib.sha256()
            with (directory / "profile.vcf").open("wb") as target:
                while chunk := stream.read(1024 * 1024):
                    size += len(chunk)
                    if size > self.max_bytes:
                        raise GeneAnalysisError("Файл превышает допустимый размер.", 413)
                    digest.update(chunk)
                    target.write(chunk)
            parsed = parse_vcf(directory / "profile.vcf")
            profile = Profile(
                id=generation, filename=filename, size_bytes=size, sha256=digest.hexdigest(),
                uploaded_at=datetime.now(timezone.utc), sample_name=parsed.sample_name,
                build_source=parsed.build_source,
            )
            metadata = profile.model_dump(mode="json")
            atomic_json(directory / "metadata.json", metadata)
            atomic_json(patient_dir / "current.json", metadata)
            installed = True
            # Очищаем также поколения, оставшиеся после аварийного завершения.
            for previous in patient_dir.iterdir():
                if previous.is_dir() and previous != directory:
                    self._remove_directory(previous)
            return profile
        finally:
            if not installed:
                self._remove_directory(directory)

    def read_report(self, patient_id: int, profile: Profile) -> GeneAnalysisReport | None:
        path = self.profile_dir(patient_id, profile) / "analysis.json"
        try:
            report = GeneAnalysisReport.model_validate_json(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return None
        except (ValidationError, UnicodeError) as exc:
            raise GeneAnalysisError("Сохранённый отчёт несовместим или повреждён; загрузите VCF повторно.", 409) from exc
        if report.patient_id != patient_id or report.profile != profile:
            raise GeneAnalysisError("Отчёт не соответствует текущему профилю; загрузите VCF повторно.", 409)
        return report

    def save_report(self, report: GeneAnalysisReport) -> None:
        path = self.profile_dir(report.patient_id, report.profile) / "analysis.json"
        atomic_json(path, report.model_dump(mode="json"))

    def delete(self, patient_id: int) -> None:
        """Удаляет только данные выбранного пациента; вызывается под lock."""
        self._remove_directory(self.patient_dir(patient_id))

    def _remove_directory(self, path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_relative_to(self.root / "patients"):
            raise ValueError("Каталог удаления вне хранилища пациентов")
        if path.exists():
            shutil.rmtree(path)
