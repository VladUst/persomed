import hashlib
import json
import re
import tempfile
import time
from pathlib import Path
import pandas as pd
import requests
from .config import ANNOTATION_CACHE_DIR


ANNOTATION_URL = "https://myvariant.info/v1/query/"


ANNOTATION_PARAMS = {
    "scopes": "dbsnp.rsid",
    "fields": "clinvar,gwas,dbsnp.gene,cadd.phred",
    "assembly": "hg19",
}


ANNOTATION_ATTEMPTS = 5


class AnnotationError(RuntimeError):
    """Аннотация не завершена; частичные данные нельзя считать полным отчётом."""


def _valid_annotation_batch(results: object, batch: list[str]) -> bool:
    """Для каждого rsID нужен ответ, включая явный notfound."""
    return (
        isinstance(results, list)
        and all(
            isinstance(hit, dict)
            and isinstance(hit.get("query"), str)
            and (hit.get("notfound") is True or bool(hit.get("_id")))
            and "error" not in hit
            for hit in results
        )
        and {hit["query"] for hit in results} == set(batch)
    )


def _query_annotation_batch(session: requests.Session, batch: list[str]) -> list[dict]:
    """Повторяет временные сетевые ошибки, не маскируя их как notfound."""
    for attempt in range(1, ANNOTATION_ATTEMPTS + 1):
        try:
            response = session.post(
                ANNOTATION_URL,
                data={**ANNOTATION_PARAMS, "q": ",".join(batch)},
                timeout=(10, 60),
            )
            response.raise_for_status()
            results = response.json()
            if not _valid_annotation_batch(results, batch):
                raise ValueError("неполный или некорректный ответ MyVariant.info")
            return results
        except (requests.RequestException, ValueError) as exc:
            status = exc.response.status_code if isinstance(exc, requests.HTTPError) else None
            reason = f"HTTP {status}" if status is not None else type(exc).__name__
            retryable = status is None or status in {408, 429} or status >= 500
            if not retryable or attempt == ANNOTATION_ATTEMPTS:
                raise AnnotationError(
                    f"MyVariant.info: {reason}. Аннотация не завершена. "
                    "Успешные пакеты сохранены; загрузите профиль повторно для нового анализа."
                ) from exc
            delay = 2 ** attempt
            if isinstance(exc, requests.HTTPError):
                retry_after = exc.response.headers.get("Retry-After", "")
                if retry_after.isdigit():
                    delay = max(delay, int(retry_after))
            time.sleep(min(delay, 60))
    raise AssertionError("Число попыток должно быть положительным")


def annotate_variants(
    variants_df: pd.DataFrame,
    *,
    cache_dir: Path = ANNOTATION_CACHE_DIR,
    batch_size: int = 500,
) -> list[dict]:
    """Отправляет rsID в MyVariant.info и возвращает аннотации.

    Запрашивает данные из ClinVar, dbSNP, GWAS Catalog, CADD.
    Аннотирует только варианты с мутациями (не homozygous_ref).
    """
    mutated = variants_df[variants_df["zygosity"] != "homozygous_ref"]
    if not 1 <= batch_size <= 1000:
        raise ValueError("Размер пакета должен быть от 1 до 1000")
    valid_ids = [
        rsid for rsid in mutated["rsid"]
        if isinstance(rsid, str) and re.fullmatch(r"rs[0-9]+", rsid)
    ]
    rsid_list = sorted(set(valid_ids))

    if not rsid_list:
        return []

    cache_dir.mkdir(parents=True, exist_ok=True)
    results = []
    requested = False
    with requests.Session() as session:
        for start in range(0, len(rsid_list), batch_size):
            batch = rsid_list[start:start + batch_size]
            key = json.dumps(
                {"version": 1, "url": ANNOTATION_URL, "params": ANNOTATION_PARAMS, "ids": batch},
                sort_keys=True,
            )
            cache_file = cache_dir / f"{hashlib.sha256(key.encode()).hexdigest()}.json"
            hits = None
            if cache_file.exists():
                try:
                    hits = json.loads(cache_file.read_text(encoding="utf-8"))
                except (ValueError, UnicodeError):
                    pass  # Повреждённый кэш перечитываем из сервиса.
            cached = _valid_annotation_batch(hits, batch)
            if not cached:
                if requested:
                    time.sleep(1)
                hits = _query_annotation_batch(session, batch)
                requested = True
                # Атомарная замена: прерывание записи не портит готовый кэш.
                temp = tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=cache_dir, suffix=".tmp", delete=False,
                )
                temp_path = Path(temp.name)
                try:
                    with temp:
                        json.dump(hits, temp, ensure_ascii=False)
                    temp_path.replace(cache_file)
                finally:
                    temp_path.unlink(missing_ok=True)
            results.extend(hits)

    return results
