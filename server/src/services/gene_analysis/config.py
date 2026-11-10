"""Пути изменяемых данных отделены от кода и ресурсов правил."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "var" / "gene_analysis"
PGS_CACHE_DIR = DATA_DIR / "cache" / "pgs"
ANNOTATION_CACHE_DIR = DATA_DIR / "cache" / "myvariant"
REFERENCE_FILE = PGS_CACHE_DIR / "eur_1000g_phase3_grch37.npz"
RESOURCES = Path(__file__).parent / "resources"
MAX_PROFILE_BYTES = int(os.environ.get("GENE_PROFILE_MAX_BYTES", 100 * 1024 * 1024))
ANALYSIS_VERSION = "1.0"
