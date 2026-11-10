"""Импорт существующих справочных кэшей без удаления исходных файлов.

Запуск: python -m src.services.gene_analysis.cache_import
"""

import json
import shutil
import tempfile
from pathlib import Path
from zipfile import BadZipFile

import numpy as np
import pandas as pd

from .annotations import _valid_annotation_batch
from .config import DATA_DIR, PROJECT_ROOT
from .pgs_catalog import DEFAULT_PGS_SCORES, valid_scoring_file


def validate_reference(path: Path) -> None:
    """Проверяет структуру NPZ до численных расчётов, не разрешая pickle."""
    with np.load(path, allow_pickle=False) as data:
        ids, samples = data["rsids"], data["samples"]
        if (ids.ndim != 1 or samples.ndim != 1 or len(samples) < 2
                or len(set(ids.tolist())) != len(ids)
                or data["alleles"].shape != (len(ids), len(samples), 2)
                or data["chrom"].shape != ids.shape or data["pos"].shape != ids.shape):
            raise ValueError("Некорректная структура EUR-референса")


def _valid(path: Path) -> bool:
    try:
        if path.suffix == ".npz":
            validate_reference(path)
            return True
        if path.suffix == ".tsv":
            return valid_scoring_file(pd.read_csv(path, sep="\t"), path.name.split("_")[0])
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            ids = [row["query"] for row in data]
            return bool(ids) and _valid_annotation_batch(data, ids)
    except (ValueError, KeyError, TypeError, OSError, EOFError, BadZipFile):
        return False
    return False


def import_caches(source: Path, destination: Path = DATA_DIR) -> int:
    """Копирует только известные модели, референс и валидные пакеты аннотаций."""
    files = [(source / ".pgs_cache" / f"{model['pgs_id']}_GRCh37.tsv", "pgs") for model in DEFAULT_PGS_SCORES]
    files.append((source / ".pgs_cache" / "eur_1000g_phase3_grch37.npz", "pgs"))
    files.extend((path, "myvariant") for path in (source / ".myvariant_cache").glob("*.json"))
    copied = 0
    for path, category in files:
        target = destination / "cache" / category / path.name
        if not path.exists() or (target.exists() and _valid(target)) or not _valid(path):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=target.parent, suffix=".tmp", delete=False) as temporary:
            staging = Path(temporary.name)
        try:
            shutil.copyfile(path, staging)
            staging.replace(target)
        finally:
            staging.unlink(missing_ok=True)
        copied += 1
    return copied


if __name__ == "__main__":
    print(f"Импортировано файлов: {import_caches(PROJECT_ROOT / 'scripts' / 'genes_analysis')}")
