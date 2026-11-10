"""Однократно извлекает EUR генотипы 1000 Genomes для выбранных PGS.

В сеть отправляются только публичные rsID из файлов PGS Catalog, не VCF пациента.
Запуск: python -m src.services.gene_analysis.prepare_reference
"""

import json
import re
import time
import tempfile
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from .pgs_catalog import DEFAULT_PGS_SCORES, download_pgs_scoring_file
from .config import PGS_CACHE_DIR
from .profile_storage import atomic_json
from .cache_import import validate_reference


CACHE = PGS_CACHE_DIR
BATCH_CACHE = CACHE / "eur_1000g_batches"
OUTPUT = CACHE / "eur_1000g_phase3_grch37.npz"
PANEL_URL = (
    "https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/"
    "integrated_call_samples_v3.20130502.ALL.panel"
)
API_URL = "https://grch37.rest.ensembl.org/variation/human"
BATCH_SIZE = 10


def _expected_variants() -> dict[str, tuple[str, int]]:
    expected = {}
    ambiguous = set()
    for model in DEFAULT_PGS_SCORES:
        scoring = download_pgs_scoring_file(model["pgs_id"])
        if scoring is None:
            raise RuntimeError(f"Нет файла весов: {model['pgs_id']}")
        for row in scoring.itertuples(index=False):
            rsid = getattr(row, "hm_rsID", None)
            chrom = getattr(row, "hm_chr", None)
            pos = getattr(row, "hm_pos", None)
            if not isinstance(rsid, str) or not re.fullmatch(r"rs\d+", rsid):
                continue
            if pd.isna(chrom) or pd.isna(pos):
                continue
            coordinate = (str(chrom).removesuffix(".0").removeprefix("chr"), int(pos))
            if rsid in expected and expected[rsid] != coordinate:
                ambiguous.add(rsid)
            expected[rsid] = coordinate
    for rsid in ambiguous:
        del expected[rsid]
    print(f"Публичных SNP для загрузки: {len(expected)}; неоднозначных rsID: {len(ambiguous)}")
    return expected


def _eur_samples(session: requests.Session) -> list[str]:
    response = session.get(PANEL_URL, timeout=30)
    response.raise_for_status()
    rows = [line.split("\t") for line in response.text.splitlines()[1:]]
    samples = [row[0] for row in rows if len(row) >= 3 and row[2] == "EUR"]
    if len(samples) < 400:
        raise ValueError("Неожиданно мало EUR-образцов в панели 1000 Genomes")
    return samples


def _fetch_batch(session: requests.Session, rsids: list[str]) -> dict:
    for attempt in range(3):
        try:
            response = session.post(
                API_URL, params={"genotypes": 1}, json={"ids": rsids},
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=(10, 120),
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict):
                raise ValueError("Некорректный ответ Ensembl")
            return data
        except (requests.RequestException, ValueError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise AssertionError("Цикл попыток должен завершиться")


def _compact_response(
    data: dict, expected: dict[str, tuple[str, int]], samples: list[str],
) -> dict:
    sample_set = set(samples)
    compact = {}
    for rsid, record in data.items():
        if rsid not in expected or not isinstance(record, dict):
            continue
        chrom, pos = expected[rsid]
        mapping = next((
            item for item in record.get("mappings", [])
            if item.get("assembly_name") == "GRCh37"
            and str(item.get("seq_region_name")) == chrom
            and item.get("start") == pos
            and item.get("strand") == 1
        ), None)
        if mapping is None:
            continue
        calls = {}
        for genotype in record.get("genotypes", []):
            sample = str(genotype.get("sample", "")).rsplit(":", 1)[-1]
            if sample not in sample_set:
                continue
            alleles = re.split(r"[|/]", str(genotype.get("genotype", "")))
            if len(alleles) == 2 and all(allele in "ACGT" and len(allele) == 1
                                         for allele in alleles):
                calls[sample] = alleles
        compact[rsid] = {"chrom": chrom, "pos": pos, "calls": calls}
    return compact


def main() -> None:
    CACHE.mkdir(parents=True, exist_ok=True)
    BATCH_CACHE.mkdir(parents=True, exist_ok=True)
    expected = _expected_variants()
    with requests.Session() as session:
        samples = _eur_samples(session)
        print(f"EUR-образцов: {len(samples)}")
        all_calls = {}
        rsids = sorted(expected)
        for index, start in enumerate(range(0, len(rsids), BATCH_SIZE), 1):
            batch = rsids[start:start + BATCH_SIZE]
            cache_file = BATCH_CACHE / f"{index:03d}.json"
            compact = None
            if cache_file.exists():
                result = json.loads(cache_file.read_text(encoding="utf-8"))
                if result.get("rsids") == batch:
                    compact = result["records"]
            if compact is None:
                data = _fetch_batch(session, batch)
                compact = _compact_response(data, expected, samples)
                atomic_json(cache_file, {"rsids": batch, "records": compact})
            all_calls.update(compact)
            print(f"Пакет {index}/{(len(rsids) + BATCH_SIZE - 1) // BATCH_SIZE}: "
                  f"получено {len(compact)}/{len(batch)} SNP", flush=True)

    retained = sorted(all_calls)
    alleles = np.zeros((len(retained), len(samples), 2), dtype="S1")
    for variant_index, rsid in enumerate(retained):
        calls = all_calls[rsid]["calls"]
        for sample_index, sample in enumerate(samples):
            if sample in calls:
                alleles[variant_index, sample_index] = calls[sample]
    with tempfile.NamedTemporaryFile(dir=CACHE, suffix=".npz", delete=False) as temporary:
        staging = Path(temporary.name)
    try:
        np.savez_compressed(
            staging, rsids=np.asarray(retained), samples=np.asarray(samples),
            chrom=np.asarray([all_calls[rsid]["chrom"] for rsid in retained]),
            pos=np.asarray([all_calls[rsid]["pos"] for rsid in retained]),
            alleles=alleles, source=np.asarray(API_URL), panel=np.asarray(PANEL_URL),
            generated=np.asarray(str(date.today())),
        )
        validate_reference(staging)
        staging.replace(OUTPUT)
    finally:
        staging.unlink(missing_ok=True)
    print(f"Готово: {OUTPUT}; {len(retained)}/{len(expected)} SNP")


if __name__ == "__main__":
    main()
