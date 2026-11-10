import gzip
import io
import tempfile
import time
from pathlib import Path
import pandas as pd
import requests
from .config import PGS_CACHE_DIR


DEFAULT_PGS_SCORES = [
    # === Болезнь Альцгеймера ===
    # Главный генетический фактор (APOE) определяется отдельно в Стадии 4.
    # PGS-скоры ниже добавляют сигнал от других вариантов помимо APOE.
    {
        "pgs_id": "PGS000025",
        "trait": "Болезнь Альцгеймера (19 SNP)",
        "trait_en": "Alzheimer's disease",
        "variants_count": 19,
    },
    {
        "pgs_id": "PGS001775",
        "trait": "Болезнь Альцгеймера (39 SNP)",
        "trait_en": "Alzheimer's disease",
        "variants_count": 39,
    },
    {
        "pgs_id": "PGS002280",
        "trait": "Болезнь Альцгеймера (83 SNP)",
        "trait_en": "Alzheimer's disease",
        "variants_count": 83,
    },

    # === Ишемическая болезнь сердца / ИБС ===
    {
        "pgs_id": "PGS000010",
        "trait": "ИБС (27 SNP)",
        "trait_en": "Coronary heart disease",
        "variants_count": 27,
    },
    {
        "pgs_id": "PGS000059",
        "trait": "ИБС (46 SNP)",
        "trait_en": "Coronary artery disease",
        "variants_count": 46,
    },
    {
        "pgs_id": "PGS000058",
        "trait": "ИБС (204 SNP)",
        "trait_en": "Coronary artery disease",
        "variants_count": 204,
    },
    {
        "pgs_id": "PGS004321",
        "trait": "ИБС (27 SNP, Marston)",
        "trait_en": "Coronary heart disease",
        "variants_count": 27,
        "source": "https://www.pgscatalog.org/score/PGS004321/",
    },
    {
        "pgs_id": "PGS000200",
        "trait": "ИБС (28 SNP)",
        "trait_en": "Coronary heart disease",
        "variants_count": 28,
        "source": "https://www.pgscatalog.org/score/PGS000200/",
    },
    # Модели диабета, астмы, мигрени, ожирения и триглицеридов сверены
    # с карточками PGS Catalog и локальным перекрытием hg19 VCF.
    {
        "pgs_id": "PGS002733",
        "trait": "Диабет 2 типа (17 SNP)",
        "trait_en": "Type 2 diabetes",
        "variants_count": 17,
        "source": "https://www.pgscatalog.org/score/PGS002733/",
    },
    {
        "pgs_id": "PGS004106",
        "trait": "Диабет 2 типа (35 SNP)",
        "trait_en": "Type 2 diabetes",
        "variants_count": 35,
        "source": "https://www.pgscatalog.org/score/PGS004106/",
    },
    {
        "pgs_id": "PGS000037",
        "trait": "Астма (15 SNP)",
        "trait_en": "Asthma",
        "variants_count": 15,
        "source": "https://www.pgscatalog.org/score/PGS000037/",
    },
    {
        "pgs_id": "PGS001281",
        "trait": "Мигрень (25 SNP)",
        "trait_en": "Migraine",
        "variants_count": 25,
        "source": "https://www.pgscatalog.org/score/PGS001281/",
    },
    {
        "pgs_id": "PGS003400",
        "trait": "Ожирение (97 SNP)",
        "trait_en": "Obesity",
        "variants_count": 97,
        "source": "https://www.pgscatalog.org/score/PGS003400/",
    },
    {
        "pgs_id": "PGS000063",
        "trait": "Уровень триглицеридов (32 SNP)",
        "trait_en": "Triglycerides",
        "variants_count": 32,
        "source": "https://www.pgscatalog.org/score/PGS000063/",
    },

]


def valid_scoring_file(frame: pd.DataFrame, pgs_id: str) -> bool:
    """Отбрасывает неподдерживаемую модель до попадания в общий кэш."""
    model = next(item for item in DEFAULT_PGS_SCORES if item["pgs_id"] == pgs_id)
    return (
        {"effect_allele", "effect_weight", "hm_chr", "hm_pos"}.issubset(frame.columns)
        and ("hm_rsID" in frame or "rsID" in frame)
        and len(frame) == model["variants_count"]
        and not any(name.startswith("dosage_") and name.endswith("_weight") for name in frame.columns)
    )


def download_pgs_scoring_file(pgs_id: str, cache_dir: Path = PGS_CACHE_DIR) -> pd.DataFrame | None:
    """Скачивает harmonized scoring-файл из PGS Catalog (GRCh37).

    Кэширует файлы локально в .pgs_cache/ чтобы не скачивать повторно.
    """
    if pgs_id not in {item["pgs_id"] for item in DEFAULT_PGS_SCORES}:
        raise ValueError("Неизвестная модель PGS")
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{pgs_id}_GRCh37.tsv"

    # Если файл уже скачан — читаем из кэша
    if cache_file.exists():
        try:
            cached = pd.read_csv(cache_file, sep="\t")
            if valid_scoring_file(cached, pgs_id):
                return cached
        except (ValueError, UnicodeError):
            pass

    url = (
        f"https://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/{pgs_id}"
        f"/ScoringFiles/Harmonized/{pgs_id}_hmPOS_GRCh37.txt.gz"
    )

    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=(10, 30))
            resp.raise_for_status()
            content = gzip.decompress(resp.content).decode("utf-8")
            break
        except requests.RequestException:
            if attempt == 2:
                return None
            time.sleep(2 ** attempt)
        except (gzip.BadGzipFile, EOFError, UnicodeError):
            return None

    # Пропускаем комментарии (#), находим строку заголовка
    lines = content.strip().split("\n")
    data_lines = [l for l in lines if not l.startswith("#")]

    if len(data_lines) < 2:
        return None

    try:
        df = pd.read_csv(io.StringIO("\n".join(data_lines)), sep="\t")
    except ValueError:
        return None
    if not valid_scoring_file(df, pgs_id):
        return None

    # Сохраняем в кэш
    with tempfile.NamedTemporaryFile(dir=cache_dir, suffix=".tmp", delete=False) as temporary:
        path = Path(temporary.name)
    try:
        df.to_csv(path, sep="\t", index=False)
        path.replace(cache_file)
    finally:
        path.unlink(missing_ok=True)
    return df
