"""
Генетический профиль пациента: анализ рисков заболеваний.

Пайплайн:
  1. Парсинг VCF-файла -> извлечение вариантов с мутациями
  2. Batch-аннотация через MyVariant.info (ClinVar, dbSNP, GWAS, CADD)
  3. Фильтрация клинически значимых вариантов (ClinVar)
  4. Проверка комплексных генотипов (APOE и др.)
  5. Полигенные шкалы риска (PGS Catalog)
  6. Сравнение PGS с EUR-референсом 1000 Genomes, если он подготовлен
  7. Форматированный отчёт и дополнительная сводка
"""

import contextlib
import gzip
import hashlib
import io
import json
import math
import os
import re
import sys
import tempfile
import time
from pathlib import Path

import pandas as pd
import requests
import vcf  # PyVCF3
import yaml
from tabulate import tabulate

# ---------------------------------------------------------------------------
# Стадия 1: Парсинг VCF (через PyVCF3)
# ---------------------------------------------------------------------------

# Маппинг gt_type PyVCF3 -> человекочитаемая зиготность
_ZYGOSITY_MAP = {
    0: "homozygous_ref",  # 0/0
    1: "heterozygous",     # 0/1 или 1/0
    2: "homozygous_alt",   # 1/1
}


def parse_vcf(vcf_path: str) -> pd.DataFrame:
    """Читает VCF-файл через PyVCF3 и возвращает DataFrame с вариантами."""
    reader = vcf.Reader(filename=vcf_path)

    records = []
    with contextlib.closing(reader._reader):
        for record in reader:
            sample = record.samples[0]
            gt_alleles = sample.gt_alleles  # ['0', '1'] или ['1', '1'] и т.д.

            if (
                gt_alleles is None or len(gt_alleles) != 2
                or any(allele is None or not str(allele).isdigit() for allele in gt_alleles)
            ):
                continue

            a1_idx, a2_idx = int(gt_alleles[0]), int(gt_alleles[1])
            zygosity = _ZYGOSITY_MAP.get(sample.gt_type, "unknown")

            # Собираем список аллелей: [REF, ALT1, ALT2, ...]
            allele_options = [record.REF] + [str(a) for a in record.ALT]
            actual_allele_1 = allele_options[a1_idx] if a1_idx < len(allele_options) else "?"
            actual_allele_2 = allele_options[a2_idx] if a2_idx < len(allele_options) else "?"

            records.append({
                "chrom": record.CHROM,
                "pos": record.POS,
                "rsid": record.ID,
                "ref": record.REF,
                "alt": ",".join(str(a) for a in record.ALT),
                "genotype": sample["GT"],
                "allele_1": actual_allele_1,
                "allele_2": actual_allele_2,
                "zygosity": zygosity,
                "phased": sample.phased,
                "phase_set": sample["PS"] if "PS" in sample.data._fields else None,
            })

    df = pd.DataFrame(records)
    print(f"[Стадия 1] Прочитано вариантов: {len(df)}")
    print(f"           С ALT-аллелем: {len(df[df['zygosity'] != 'homozygous_ref'])}")
    return df


# ---------------------------------------------------------------------------
# Стадия 2: Аннотация через MyVariant.info
# ---------------------------------------------------------------------------

ANNOTATION_CACHE_DIR = Path(__file__).parent / ".myvariant_cache"
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
                    "Успешные пакеты сохранены; повторите ту же команду позже."
                ) from exc
            delay = 2 ** attempt
            if isinstance(exc, requests.HTTPError):
                retry_after = exc.response.headers.get("Retry-After", "")
                if retry_after.isdigit():
                    delay = max(delay, int(retry_after))
            print(
                f"    {reason}, попытка {attempt}/{ANNOTATION_ATTEMPTS}; "
                f"повтор через {delay} с.", flush=True,
            )
            time.sleep(delay)
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
    invalid_count = len(mutated) - len(valid_ids)
    if invalid_count:
        print(f"           Пропущено записей без одиночного rsID: {invalid_count}")

    if not rsid_list:
        print("[Стадия 2] Нет вариантов с мутациями и корректным rsID для аннотации.")
        return []

    total_batches = math.ceil(len(rsid_list) / batch_size)
    print(
        f"[Стадия 2] Аннотация {len(rsid_list)} уникальных rsID: "
        f"{total_batches} пакетов, до {batch_size} rsID в каждом.", flush=True,
    )
    cache_dir.mkdir(parents=True, exist_ok=True)
    results = []
    requested = False
    with requests.Session() as session:
        for index, start in enumerate(range(0, len(rsid_list), batch_size), 1):
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
                print(f"    Пакет {index}/{total_batches}: запрос...", flush=True)
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
            completed = min(start + batch_size, len(rsid_list))
            source = "кэш" if cached else "сервис, сохранено"
            print(
                f"    Пакет {index}/{total_batches}: {source}; "
                f"обработано {completed}/{len(rsid_list)} rsID.", flush=True,
            )

    found = {r["query"] for r in results if not r.get("notfound", False)}
    print(f"           rsID с аннотациями: {len(found)} из {len(rsid_list)}")
    return results


# ---------------------------------------------------------------------------
# Стадия 3: Анализ клинической значимости (ClinVar)
# ---------------------------------------------------------------------------

CLINVAR_CATEGORIES = {
    "pathogenic": "Кандидат для проверки",
    "likely pathogenic": "Кандидат для проверки",
    "pathogenic/likely pathogenic": "Кандидат для проверки",
    "conflicting interpretations of pathogenicity": "Спорное заключение",
    "uncertain significance": "Неопределённая значимость",
    "risk factor": "Ассоциация",
    "association": "Ассоциация",
    "affects": "Ассоциация",
    "drug response": "Фармакогенетика",
}


def _matching_snv(annotation: dict, variant: dict) -> bool:
    """Проверяет hg19 SNV, включая альтернативный аллель в генотипе."""
    clinvar = annotation.get("clinvar")
    if not isinstance(clinvar, dict):
        return False
    chrom = str(variant["chrom"]).removeprefix("chr")
    ref, alt = str(variant["ref"]).upper(), str(variant["alt"]).upper()
    if len(ref) != 1 or len(alt) != 1 or ref not in "ACGT" or alt not in "ACGT":
        return False
    if alt not in {variant["allele_1"], variant["allele_2"]}:
        return False
    position = int(variant["pos"])
    hg19 = clinvar.get("hg19")
    return (
        annotation.get("_id") == f"chr{chrom}:g.{position}{ref}>{alt}"
        and str(clinvar.get("chrom")) == chrom
        and clinvar.get("ref") == ref
        and clinvar.get("alt") == alt
        and isinstance(hg19, dict)
        and hg19.get("start") == position
        and hg19.get("end") == position
    )


def extract_clinvar_significance(annotations: list[dict], variants_df: pd.DataFrame) -> pd.DataFrame:
    """Возвращает ClinVar-записи только для точно сопоставленных hg19 SNP."""
    clinvar_records = []
    annotated_ids = {
        ann.get("query") for ann in annotations
        if isinstance(ann.get("clinvar"), dict)
    }
    variants_by_rsid = {}
    for variant in variants_df[variants_df["rsid"].isin(annotated_ids)].to_dict("records"):
        variants_by_rsid.setdefault(variant["rsid"], []).append(variant)
    unmatched = 0

    for ann in annotations:
        if ann.get("notfound"):
            continue

        query_rsid = ann.get("query", "")
        clinvar = ann.get("clinvar")
        if not isinstance(clinvar, dict):
            continue
        matching = [
            variant for variant in variants_by_rsid.get(query_rsid, [])
            if _matching_snv(ann, variant)
        ]
        if len(matching) != 1:
            unmatched += 1
            continue
        variant = matching[0]

        # ClinVar может вернуть один объект или список
        rcv_list = clinvar.get("rcv", [])
        if isinstance(rcv_list, dict):
            rcv_list = [rcv_list]

        for rcv in rcv_list:
            significance = rcv.get("clinical_significance", "")
            if not isinstance(significance, str):
                continue
            category = CLINVAR_CATEGORIES.get(significance.strip().casefold())
            if category is None:
                continue
            conditions = rcv.get("conditions", {})
            condition_name = ""

            if isinstance(conditions, dict):
                condition_name = conditions.get("name", "")
            elif isinstance(conditions, list):
                condition_name = "; ".join(
                    c.get("name", "") for c in conditions if isinstance(c, dict)
                )

            gene_info = clinvar.get("gene", {})
            gene_name = ""
            if isinstance(gene_info, dict):
                gene_name = gene_info.get("symbol", "")
            elif isinstance(gene_info, list):
                gene_name = ", ".join(
                    g.get("symbol", "") for g in gene_info if isinstance(g, dict)
                )

            clinvar_records.append({
                "rsid": query_rsid,
                "variant": ann["_id"],
                "clinvar_id": rcv.get("accession", ""),
                "gene": gene_name,
                "significance": significance,
                "category": category,
                "condition": condition_name,
                "genotype": f"{variant['allele_1']}/{variant['allele_2']}",
                "zygosity": variant["zygosity"],
                "review_status": rcv.get("review_status", ""),
                "last_evaluated": rcv.get("last_evaluated", ""),
            })

    df = pd.DataFrame(clinvar_records)
    if not df.empty:
        df = df.drop_duplicates(subset=["variant", "clinvar_id", "significance", "condition"])
    print(f"[Стадия 3] Точно сопоставленных записей ClinVar: {len(df)}")
    print(f"           Пропущено аннотаций без точного совпадения hg19 SNP: {unmatched}")
    df.attrs["unmatched_annotations"] = unmatched
    return df


# ---------------------------------------------------------------------------
# Стадия 4: Комплексные генотипы (загружаются из complex_genotypes.yaml)
# ---------------------------------------------------------------------------

# Правила определены декларативно в complex_genotypes.yaml — добавлять
# новые гаплотипы можно без правки Python.
#
# Поддерживаются два типа правил:
#   - "snp"       — один SNP, риск зависит от числа копий risk_allele (0/1/2)
#   - "haplotype" — несколько SNP комбинируются в гаплотип (как APOE ε2/ε3/ε4)

COMPLEX_GENOTYPES_YAML = Path(__file__).parent / "complex_genotypes.yaml"


def _load_complex_rules() -> list[dict]:
    """Загружает правила из YAML. Возвращает [], если файл отсутствует."""
    if not COMPLEX_GENOTYPES_YAML.exists():
        return []
    with open(COMPLEX_GENOTYPES_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("rules", [])


def _format_details(risk_info: dict) -> str:
    """Собирает details + OR (если есть) в одну строку."""
    details = risk_info.get("details", "")
    or_val = risk_info.get("or")
    if or_val is not None and "OR" not in details:
        or_str = f"OR ≈ {or_val}"
        return "; ".join(filter(None, [details, or_str]))
    return details


def _call_haplotype(rule: dict, snp_to_allele: dict) -> str:
    """Определяет имя гаплотипа по аллелям на одной хромосоме."""
    for hap in rule.get("haplotype_rules", []):
        required = hap["alleles"]
        if all(snp_to_allele.get(snp) == al for snp, al in required.items()):
            return hap["name"]
    return "?"


def _eval_haplotype_rule(rule: dict, genotype_lookup: dict) -> dict | None:
    """Объединяет несколько SNP в диплотип (например, e3/e4)."""
    required = rule.get("required_snps", [])
    missing = [snp for snp in required if snp not in genotype_lookup]
    disease = next(iter(rule.get("diplotype_risk", {}).values()), {}).get("disease", "")
    if missing:
        return {
            "gene": rule["name"], "genotype": "—", "disease": disease,
            "risk_level": "Не оценено", "status": "Не оценено",
            "details": f"В VCF отсутствует: {', '.join(missing)}",
        }

    heterozygous = [
        snp for snp in required
        if genotype_lookup[snp][0] != genotype_lookup[snp][1]
    ]
    if len(heterozygous) > 1:
        phase_sets = {genotype_lookup[snp][3] for snp in heterozygous}
        phased = all(genotype_lookup[snp][2] for snp in heterozygous)
        if not phased or None in phase_sets or len(phase_sets) != 1:
            return {
                "gene": rule["name"], "genotype": "—", "disease": disease,
                "risk_level": "Не оценено", "status": "Не оценено",
                "details": "Фаза между вариантами не подтверждена",
            }

    hap1 = _call_haplotype(rule, {snp: genotype_lookup[snp][0] for snp in required})
    hap2 = _call_haplotype(rule, {snp: genotype_lookup[snp][1] for snp in required})
    diplotype = "/".join(sorted([hap1, hap2]))

    risk = rule.get("diplotype_risk", {}).get(diplotype)
    if not risk:
        return {
            "gene": rule["name"], "genotype": diplotype, "disease": disease,
            "risk_level": "Не оценено", "status": "Не оценено",
            "details": "Для этого диплотипа нет правила интерпретации",
        }

    return {
        "gene": rule["name"],
        "genotype": diplotype,
        "disease": risk["disease"],
        "risk_level": risk["level"],
        "status": "Оценено по правилу",
        "details": _format_details(risk),
    }


def _eval_snp_rule(rule: dict, genotype_lookup: dict) -> dict | None:
    """Один SNP — риск по числу копий risk_allele."""
    rsid = rule.get("snp")
    if rsid not in genotype_lookup:
        disease = next(iter(rule.get("genotypes", {}).values()), {}).get("disease", "")
        return {
            "gene": rule["name"], "genotype": "—", "disease": disease,
            "risk_level": "Не оценено", "status": "Не оценено",
            "details": f"В VCF отсутствует {rsid}",
        }

    risk_allele = rule.get("risk_allele")
    a1, a2 = genotype_lookup[rsid][:2]
    ref, alt = genotype_lookup[rsid][4:6]
    if risk_allele not in {ref, alt}:
        return {
            "gene": rule["name"], "genotype": f"{a1}/{a2}",
            "disease": next(iter(rule.get("genotypes", {}).values()), {}).get("disease", ""),
            "risk_level": "Не оценено", "status": "Не оценено",
            "details": f"Аллель {risk_allele} отсутствует среди REF/ALT для {rsid}",
        }
    n_risk = (1 if a1 == risk_allele else 0) + (1 if a2 == risk_allele else 0)
    gt_key = {0: "0/0", 1: "0/1", 2: "1/1"}[n_risk]

    risk = rule.get("genotypes", {}).get(gt_key)
    if not risk:
        return None

    return {
        "gene": rule["name"],
        "genotype": f"{a1}/{a2}",
        "disease": risk["disease"],
        "risk_level": risk["level"],
        "status": "Оценено по правилу",
        "details": _format_details(risk),
    }


def evaluate_complex_genotypes(variants_df: pd.DataFrame) -> list[dict]:
    """Применяет все правила из YAML к генотипам пациента."""
    rules = _load_complex_rules()

    genotype_lookup = {}
    for _, row in variants_df.iterrows():
        genotype_lookup[row["rsid"]] = (
            row["allele_1"], row["allele_2"],
            bool(row.get("phased", False)), row.get("phase_set"),
            row["ref"], row["alt"],
        )

    results = []
    for rule in rules:
        rtype = rule.get("type", "snp")
        if rtype == "haplotype":
            result = _eval_haplotype_rule(rule, genotype_lookup)
        elif rtype == "snp":
            result = _eval_snp_rule(rule, genotype_lookup)
        else:
            continue
        if result:
            results.append(result)

    assessed = sum(result["status"] != "Не оценено" for result in results)
    print(f"[Стадия 4] Правил оценено: {assessed}; не оценено: {len(results) - assessed}")
    return results


# ---------------------------------------------------------------------------
# Стадия 5: Полигенные шкалы риска (PGS Catalog)
# ---------------------------------------------------------------------------

def _coverage_label(coverage_pct: float) -> tuple[str, bool]:
    """Порог отображения исследовательского расчёта, не клинической оценки."""
    if coverage_pct >= 75:
        return "Измерено ≥75% SNP", True
    if coverage_pct >= 30:
        return "Измерено 30–74% SNP", True
    return "Измерено <30% SNP", False


# Набор PGS-моделей с проверенным соответствием ID и признака.
# Сумма весов не даёт клинически валидированного перцентиля.
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

# Директория для кэширования scoring-файлов
PGS_CACHE_DIR = Path(__file__).parent / ".pgs_cache"


def download_pgs_scoring_file(pgs_id: str) -> pd.DataFrame | None:
    """Скачивает harmonized scoring-файл из PGS Catalog (GRCh37).

    Кэширует файлы локально в .pgs_cache/ чтобы не скачивать повторно.
    """
    PGS_CACHE_DIR.mkdir(exist_ok=True)
    cache_file = PGS_CACHE_DIR / f"{pgs_id}_GRCh37.tsv"

    # Если файл уже скачан — читаем из кэша
    if cache_file.exists():
        return pd.read_csv(cache_file, sep="\t")

    url = (
        f"https://ftp.ebi.ac.uk/pub/databases/spot/pgs/scores/{pgs_id}"
        f"/ScoringFiles/Harmonized/{pgs_id}_hmPOS_GRCh37.txt.gz"
    )

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"    Ошибка загрузки {pgs_id}: {e}")
        return None

    content = gzip.decompress(resp.content).decode("utf-8")

    # Пропускаем комментарии (#), находим строку заголовка
    lines = content.strip().split("\n")
    data_lines = [l for l in lines if not l.startswith("#")]

    if len(data_lines) < 2:
        return None

    df = pd.read_csv(io.StringIO("\n".join(data_lines)), sep="\t")

    # Сохраняем в кэш
    df.to_csv(cache_file, sep="\t", index=False)
    return df


def _pgs_alleles_match(pgs_row: pd.Series, variant: dict, effect_allele: str) -> bool:
    """Не переносит вес REF-аллеля на другую замену в том же rsID."""
    ref, alt = str(variant["ref"]).upper(), str(variant["alt"]).upper()
    if len(ref) != 1 or len(alt) != 1 or ref not in "ACGT" or alt not in "ACGT":
        return False
    if effect_allele not in {ref, alt}:
        return False
    other = pgs_row.get("other_allele")
    if other is None or pd.isna(other):
        other = pgs_row.get("hm_inferOtherAllele")
    other = str(other).upper() if other is not None and not pd.isna(other) else ""
    if other in {"A", "C", "G", "T"}:
        return {effect_allele, other} == {ref, alt}
    # Если эффекторный аллель = ALT, замена определена однозначно.
    # Для эффекторного REF без второго аллеля вариантов может быть несколько.
    return effect_allele == alt


def calculate_pgs(
    variants_df: pd.DataFrame,
    scoring_df: pd.DataFrame,
) -> dict:
    """Исследовательская сумма весов; 2*EAF только для отсутствующих SNP.

    Без подходящей референсной выборки сумма не переводится в персональный
    перцентиль или вероятность заболевания.
    """
    rsid_col = "hm_rsID" if "hm_rsID" in scoring_df.columns else "rsID"
    if rsid_col not in scoring_df.columns:
        return {
            "matched": 0, "imputed": 0, "skipped": 0, "total": 0,
            "score": 0.0, "coverage_pct": 0, "effective_coverage_pct": 0,
        }

    eaf_col = "allelefrequency_effect"
    has_eaf = eaf_col in scoring_df.columns

    if any(
        column.startswith("dosage_") and column.endswith("_weight")
        for column in scoring_df.columns
    ):
        raise ValueError("Модель с весами по дозировкам не поддерживается")

    relevant_ids = set(scoring_df[rsid_col].dropna())
    vcf_lookup = {}
    for row in variants_df[variants_df["rsid"].isin(relevant_ids)].to_dict("records"):
        vcf_lookup.setdefault(row["rsid"], []).append(row)

    total_snps = len(scoring_df)
    matched = 0   # SNP реально измерен у пациента
    imputed = 0   # SNP не измерен, но подставлено среднее по популяции
    skipped = 0   # SNP не измерен и нет EAF — нельзя ничего сказать
    score = 0.0
    for _, pgs_row in scoring_df.iterrows():
        rsid = pgs_row.get(rsid_col, "")
        if not isinstance(rsid, str) or not re.fullmatch(r"rs[0-9]+", rsid):
            skipped += 1
            continue

        effect_allele = str(pgs_row.get("effect_allele", "")).upper()
        if effect_allele not in {"A", "C", "G", "T"}:
            skipped += 1
            continue
        weight = pgs_row.get("effect_weight", 0.0)
        if pd.isna(weight):
            skipped += 1
            continue
        w = float(weight)

        eaf_raw = pgs_row.get(eaf_col) if has_eaf else None
        eaf_valid = (
            eaf_raw is not None
            and not pd.isna(eaf_raw)
            and 0 < float(eaf_raw) < 1
        )
        eaf = float(eaf_raw) if eaf_valid else None

        # rsID не доказывает совпадение аллеля: сверяем координату GRCh37,
        # REF/ALT и эффектный аллель. Неоднозначные записи не считаем измеренными.
        chrom = pgs_row.get("hm_chr")
        pos = pgs_row.get("hm_pos")
        if pd.isna(chrom) or pd.isna(pos):
            skipped += 1
            continue
        else:
            chrom = str(chrom).removesuffix(".0").removeprefix("chr")
            candidates = [
                row for row in vcf_lookup.get(rsid, [])
                if str(row["chrom"]).removeprefix("chr") == chrom
                and int(row["pos"]) == int(pos)
                and _pgs_alleles_match(pgs_row, row, effect_allele)
            ]
        if len(candidates) == 1:
            row = candidates[0]
            dosage = (row["allele_1"] == effect_allele) + (row["allele_2"] == effect_allele)
            score += w * dosage
            matched += 1
        elif vcf_lookup.get(rsid):
            # rsID есть в VCF, но координата/аллели не сходятся или запись
            # неоднозначна. Популяционное среднее скрывало бы эту ошибку.
            skipped += 1
        elif eaf_valid:
            score += w * 2 * eaf
            imputed += 1
        else:
            # Без EAF отсутствующий SNP не восстанавливается: итоговая
            # сумма остаётся частичной и не сравнивается с полной моделью.
            skipped += 1

    raw_cov = round(matched / total_snps * 100, 1) if total_snps > 0 else 0
    eff_cov = round((matched + imputed) / total_snps * 100, 1) if total_snps > 0 else 0

    return {
        "matched": matched,
        "imputed": imputed,
        "skipped": skipped,
        "total": total_snps,
        "score": round(score, 6),
        "coverage_pct": raw_cov,
        "effective_coverage_pct": eff_cov,
    }


def compute_pgs_scores(
    variants_df: pd.DataFrame,
    pgs_list: list[dict] | None = None,
) -> list[dict]:
    """Рассчитывает исследовательские суммы только для простых моделей."""
    if pgs_list is None:
        pgs_list = DEFAULT_PGS_SCORES

    print(f"[Стадия 5] Проверка полигенных моделей ({len(pgs_list)})...")

    results = []
    for pgs_info in pgs_list:
        pgs_id = pgs_info["pgs_id"]
        trait = pgs_info["trait"]

        scoring_df = download_pgs_scoring_file(pgs_id)
        if scoring_df is None:
            results.append({"pgs_id": pgs_id, "trait": trait, "status": "Не оценено",
                            "reason": "Не удалось загрузить файл весов"})
            continue

        required = {"effect_allele", "effect_weight", "hm_chr", "hm_pos"}
        if not required.issubset(scoring_df.columns) or any(
            column.startswith("dosage_") and column.endswith("_weight")
            for column in scoring_df.columns
        ) or len(scoring_df) != pgs_info.get("variants_count"):
            results.append({"pgs_id": pgs_id, "trait": trait, "status": "Не оценено",
                            "reason": "Формат или размер файла весов не соответствует поддерживаемой модели"})
            continue

        calc = calculate_pgs(variants_df, scoring_df)
        coverage_label, has_minimum_overlap = _coverage_label(calc["coverage_pct"])
        if not has_minimum_overlap:
            status = "Не оценено"
            reason = "Измерено менее 30% SNP модели"
        elif calc["skipped"]:
            status = "Частичная сумма весов"
            reason = f"Не учтено {calc['skipped']} SNP; сумма неполная"
        else:
            status = "Исследовательский показатель"
            reason = "Без референсной калибровки"

        results.append({
            "pgs_id": pgs_id,
            "trait": trait,
            "trait_en": pgs_info.get("trait_en", ""),
            "source": pgs_info.get("source", f"https://www.pgscatalog.org/score/{pgs_id}/"),
            "score": calc["score"],
            "matched": calc["matched"],
            "imputed": calc["imputed"],
            "skipped": calc["skipped"],
            "total": calc["total"],
            "coverage_pct": calc["coverage_pct"],
            "effective_coverage_pct": calc["effective_coverage_pct"],
            "coverage_label": coverage_label,
            "status": status,
            "reason": reason,
        })

        print(
            f"    {pgs_id}: {trait} | "
            f"измерено {calc['matched']}/{calc['total']} "
            f"({calc['coverage_pct']}%), подставлено среднее для {calc['imputed']} | "
            f"{status}"
        )

    print(f"           Моделей проверено: {len(results)}")
    return results


# ---------------------------------------------------------------------------
# Стадия 6: Форматированный вывод
# ---------------------------------------------------------------------------

def print_report(
    variants_df: pd.DataFrame,
    clinvar_df: pd.DataFrame,
    complex_results: list[dict],
    pgs_results: list[dict],
):
    """Выводит итоговый отчёт в консоль."""
    print("\n" + "=" * 70)
    print("    ГЕНЕТИЧЕСКИЙ ПРОФИЛЬ: ПРОВЕРКА ВАРИАНТОВ И ИССЛЕДОВАТЕЛЬСКИХ МОДЕЛЕЙ")
    print("=" * 70)

    # --- Сводка ---
    total = len(variants_df)
    mutated = len(variants_df[variants_df["zygosity"] != "homozygous_ref"])
    print(f"\nВсего вариантов в профиле: {total}")
    print(f"Вариантов с ALT-аллелем:  {mutated}")
    print("Генотипы и аннотации из этого отчёта не подтверждают диагноз.")

    # --- Раздел 1: Клинически значимые варианты ---
    print("\n" + "-" * 70)
    print("  1. ТОЧНО СОПОСТАВЛЕННЫЕ АННОТАЦИИ ClinVar (hg19, SNV)")
    print("-" * 70)

    if clinvar_df.empty:
        print("  Аннотаций выбранных категорий для точно совпавших SNP нет.")
        print("  Это не исключает заболевания или варианты вне проверенного набора.")
    else:
        for category in ["Кандидат для проверки", "Спорное заключение",
                         "Неопределённая значимость", "Фармакогенетика", "Ассоциация"]:
            subset = clinvar_df[clinvar_df["category"] == category]
            if subset.empty:
                continue

            print(f"\n  [{category.upper()}]")
            table_data = []
            for _, row in subset.iterrows():
                table_data.append([
                    row["variant"], row["rsid"], row["clinvar_id"],
                    row["gene"],
                    row["genotype"],
                    row["significance"],
                    row["condition"][:50],
                    row["review_status"], row["last_evaluated"],
                ])
            print(tabulate(
                table_data,
                headers=["Вариант", "rsID", "ClinVar", "Ген", "Генотип",
                         "Категория ClinVar", "Признак", "Статус проверки", "Дата"],
                tablefmt="simple",
                numalign="left",
            ))
    print(f"  Не оценено из-за отсутствия точного совпадения: "
          f"{clinvar_df.attrs.get('unmatched_annotations', 0)} аннотаций.")
    print("  'Кандидат для проверки' означает классификацию варианта в источнике,")
    print("  а не подтверждение заболевания у владельца VCF.")

    # --- Раздел 2: Комплексные генотипы ---
    print("\n" + "-" * 70)
    print("  2. КОМПЛЕКСНЫЕ ГЕНОТИПЫ")
    print("-" * 70)

    if not complex_results:
        print("  Правила отсутствуют или не применились к этому профилю.")
    else:
        for r in complex_results:
            print(f"\n  {r['gene']}: {r['genotype']}")
            print(f"    Статус:       {r['status']}")
            print(f"    Признак:      {r['disease']}")
            if r["status"] != "Не оценено":
                print(f"    Категория правила: {r['risk_level']}")
            print(f"    Подробности:  {r['details']}")
    print("  Категории правил описывают опубликованные ассоциации, не диагноз.")

    # --- Раздел 3: Полигенные шкалы риска ---
    print("\n" + "-" * 70)
    print("  3. ПОЛИГЕННЫЕ МОДЕЛИ (PGS Catalog, исследовательский расчёт)")
    print("-" * 70)

    if not pgs_results:
        print("  Полигенные модели не выбраны.")
    else:
        table_data = []
        for r in pgs_results:
            if r["status"] == "Исследовательский показатель":
                score = f"{r['score']:+.4f}"
            elif r["status"] == "Частичная сумма весов":
                score = f"{r['score']:+.4f}*"
            else:
                score = "—"
            measured = (
                f"{r['matched']}/{r['total']} ({r['coverage_pct']}%)"
                if "matched" in r else "—"
            )
            table_data.append([
                r["pgs_id"], r["trait"], measured,
                score, r["status"], r["reason"],
            ])
        print()
        print(tabulate(
            table_data,
            headers=["PGS ID", "Признак", "Измерено", "Сумма весов",
                     "Статус", "Причина"],
            tablefmt="simple", numalign="left",
        ))
        print("\n  Сумма весов — исследовательский показатель с подстановкой")
        print("  среднего 2*EAF только там, где EAF есть в файле весов.")
        print("  * — частичная сумма: не все SNP модели учтены.")
        print("  Покрытие ≥30% допускает показ исследовательской суммы, но")
        print("  не подтверждает пригодность модели для оценки риска.")
        print("  Без референсной калибровки сумма не является вероятностью")
        print("  заболевания, перцентилем или категорией риска.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Устанавливаем UTF-8 вывод для Windows-консолей
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    # Определяем путь к VCF-файлу
    script_dir = Path(__file__).parent
    default_vcf = script_dir / "genetical_profile_short.vcf"

    vcf_path = sys.argv[1] if len(sys.argv) > 1 else str(default_vcf)

    if not os.path.exists(vcf_path):
        print(f"Ошибка: файл не найден: {vcf_path}")
        sys.exit(1)

    print(f"Анализ генетического профиля: {vcf_path}\n")

    # Стадия 1: Парсинг VCF
    variants_df = parse_vcf(vcf_path)

    # Стадия 2: Аннотация через MyVariant.info
    try:
        annotations = annotate_variants(variants_df)
    except AnnotationError as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)

    # Стадия 3: Извлечение ClinVar
    clinvar_df = extract_clinvar_significance(annotations, variants_df)

    # Стадия 4: Комплексные генотипы
    complex_results = evaluate_complex_genotypes(variants_df)

    # Стадия 5: Полигенные шкалы риска
    pgs_results = compute_pgs_scores(variants_df)

    # Сравнение с индивидуальными EUR-генотипами 1000 Genomes, если референс подготовлен.
    if __package__:
        from .pgs_interpretation import interpret_pgs
    else:
        from pgs_interpretation import interpret_pgs
    pgs_results = interpret_pgs(
        variants_df, pgs_results, download_pgs_scoring_file, _pgs_alleles_match,
    )

    # Стадия 6: Отчёт
    print_report(variants_df, clinvar_df, complex_results, pgs_results)

    # Стадия 7: Дополнительная краткая сводка для клинического разбора.
    if __package__:
        from .clinical_summary import build_clinical_summary, print_clinical_summary
    else:
        from clinical_summary import build_clinical_summary, print_clinical_summary

    summary = build_clinical_summary(variants_df, clinvar_df, complex_results, pgs_results)
    print_clinical_summary(summary)


if __name__ == "__main__":
    main()
