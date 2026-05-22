"""
Генетический профиль пациента: анализ рисков заболеваний.

Пайплайн:
  1. Парсинг VCF-файла -> извлечение вариантов с мутациями
  2. Batch-аннотация через MyVariant.info (ClinVar, dbSNP, GWAS, CADD)
  3. Фильтрация клинически значимых вариантов (ClinVar)
  4. Проверка комплексных генотипов (APOE и др.)
  5. Полигенные шкалы риска (PGS Catalog)
  6. Форматированный отчёт
"""

import gzip
import io
import math
import os
import sys
from pathlib import Path

import myvariant
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
    for record in reader:
        sample = record.samples[0]
        gt_alleles = sample.gt_alleles  # ['0', '1'] или ['1', '1'] и т.д.

        if gt_alleles is None or len(gt_alleles) != 2:
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
        })

    df = pd.DataFrame(records)
    print(f"[Стадия 1] Прочитано вариантов: {len(df)}")
    print(f"           С мутациями (не 0|0): {len(df[df['zygosity'] != 'homozygous_ref'])}")
    return df


# ---------------------------------------------------------------------------
# Стадия 2: Аннотация через MyVariant.info
# ---------------------------------------------------------------------------

def annotate_variants(variants_df: pd.DataFrame) -> list[dict]:
    """Отправляет rsID в MyVariant.info и возвращает аннотации.

    Запрашивает данные из ClinVar, dbSNP, GWAS Catalog, CADD.
    Аннотирует только варианты с мутациями (не homozygous_ref).
    """
    mutated = variants_df[variants_df["zygosity"] != "homozygous_ref"]
    rsid_list = mutated["rsid"].tolist()

    if not rsid_list:
        print("[Стадия 2] Нет вариантов с мутациями для аннотации.")
        return []

    print(f"[Стадия 2] Отправляю {len(rsid_list)} rsID в MyVariant.info...")

    mv = myvariant.MyVariantInfo()
    results = mv.querymany(
        rsid_list,
        scopes="dbsnp.rsid",
        fields="clinvar,gwas,dbsnp.gene,cadd.phred",
        assembly="hg19",
        verbose=False,
    )

    found = [r for r in results if not r.get("notfound", False)]
    print(f"           Найдено аннотаций: {len(found)} из {len(rsid_list)}")
    return results


# ---------------------------------------------------------------------------
# Стадия 3: Анализ клинической значимости (ClinVar)
# ---------------------------------------------------------------------------

SIGNIFICANT_CATEGORIES = {
    "Pathogenic",
    "Likely pathogenic",
    "Pathogenic/Likely pathogenic",
    "risk factor",
    "Risk factor",
    "drug response",
    "Drug response",
    "association",
    "Affects",
}


def extract_clinvar_significance(annotations: list[dict], variants_df: pd.DataFrame) -> pd.DataFrame:
    """Извлекает клинически значимые варианты из аннотаций ClinVar."""
    clinvar_records = []

    for ann in annotations:
        if ann.get("notfound"):
            continue

        query_rsid = ann.get("query", "")
        clinvar = ann.get("clinvar")
        if not clinvar:
            continue

        # ClinVar может вернуть один объект или список
        rcv_list = clinvar.get("rcv", [])
        if isinstance(rcv_list, dict):
            rcv_list = [rcv_list]

        for rcv in rcv_list:
            significance = rcv.get("clinical_significance", "")
            conditions = rcv.get("conditions", {})
            condition_name = ""

            if isinstance(conditions, dict):
                condition_name = conditions.get("name", "")
            elif isinstance(conditions, list):
                condition_name = "; ".join(
                    c.get("name", "") for c in conditions if isinstance(c, dict)
                )

            # Фильтруем только значимые
            if any(cat.lower() in significance.lower() for cat in SIGNIFICANT_CATEGORIES):
                # Получаем ген
                gene_info = clinvar.get("gene", {})
                gene_name = ""
                if isinstance(gene_info, dict):
                    gene_name = gene_info.get("symbol", "")
                elif isinstance(gene_info, list):
                    gene_name = ", ".join(
                        g.get("symbol", "") for g in gene_info if isinstance(g, dict)
                    )

                # CADD score
                cadd = ann.get("cadd", {})
                cadd_phred = cadd.get("phred", "") if isinstance(cadd, dict) else ""

                # Генотип из исходных данных
                variant_row = variants_df[variants_df["rsid"] == query_rsid]
                genotype = ""
                zygosity = ""
                if not variant_row.empty:
                    genotype = f"{variant_row.iloc[0]['allele_1']}/{variant_row.iloc[0]['allele_2']}"
                    zygosity = variant_row.iloc[0]["zygosity"]

                clinvar_records.append({
                    "rsid": query_rsid,
                    "gene": gene_name,
                    "significance": significance,
                    "condition": condition_name,
                    "genotype": genotype,
                    "zygosity": zygosity,
                    "cadd_phred": cadd_phred,
                })

    df = pd.DataFrame(clinvar_records)
    if not df.empty:
        df = df.drop_duplicates(subset=["rsid", "condition"])
    print(f"[Стадия 3] Клинически значимых записей: {len(df)}")
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
    if any(snp not in genotype_lookup for snp in required):
        return None

    hap1 = _call_haplotype(rule, {snp: genotype_lookup[snp][0] for snp in required})
    hap2 = _call_haplotype(rule, {snp: genotype_lookup[snp][1] for snp in required})
    diplotype = "/".join(sorted([hap1, hap2]))

    risk = rule.get("diplotype_risk", {}).get(diplotype)
    if not risk:
        return None

    return {
        "gene": rule["name"],
        "genotype": diplotype,
        "disease": risk["disease"],
        "risk_level": risk["level"],
        "details": _format_details(risk),
    }


def _eval_snp_rule(rule: dict, genotype_lookup: dict) -> dict | None:
    """Один SNP — риск по числу копий risk_allele."""
    rsid = rule.get("snp")
    if rsid not in genotype_lookup:
        return None

    risk_allele = rule.get("risk_allele")
    a1, a2 = genotype_lookup[rsid]
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
        "details": _format_details(risk),
    }


def evaluate_complex_genotypes(variants_df: pd.DataFrame) -> list[dict]:
    """Применяет все правила из YAML к генотипам пациента."""
    rules = _load_complex_rules()

    genotype_lookup = {}
    for _, row in variants_df.iterrows():
        genotype_lookup[row["rsid"]] = (row["allele_1"], row["allele_2"])

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

    print(f"[Стадия 4] Комплексных генотипов определено: {len(results)}")
    return results


# ---------------------------------------------------------------------------
# Стадия 5: Полигенные шкалы риска (PGS Catalog)
# ---------------------------------------------------------------------------

def _norm_cdf(z: float) -> float:
    """Стандартное нормальное распределение через math.erf."""
    return (1.0 + math.erf(z / math.sqrt(2))) / 2


def _risk_tier(percentile: float) -> tuple[str, str]:
    """Перцентиль → уровень риска и индикатор."""
    if percentile >= 95:
        return "Очень высокий", "▲▲▲"
    if percentile >= 80:
        return "Повышенный", "▲▲"
    if percentile >= 60:
        return "Умеренно повышенный", "▲"
    if percentile >= 40:
        return "Средний", "—"
    if percentile >= 20:
        return "Умеренно пониженный", "▽"
    return "Пониженный", "▽▽"


def _coverage_label(coverage_pct: float) -> tuple[str, bool]:
    """Покрытие → метка надёжности и флаг достаточности."""
    if coverage_pct >= 80:
        return "Высокое", True
    if coverage_pct >= 50:
        return "Среднее", True
    if coverage_pct >= 20:
        return "Низкое", False
    return "Недостаточное", False


# Набор PGS-скоров для расчёта.
# Фокус: Болезнь Альцгеймера, ИБС, Сахарный диабет 2 типа.
# Все ID проверены через check_pgs_candidates.py на наличие EAF —
# это необходимо для расчёта перцентилей через z-score.
# Для каждого заболевания берём несколько скоров разного размера:
# если они дают согласованный перцентиль — результат надёжнее.
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

    # === Сахарный диабет 2 типа ===
    {
        "pgs_id": "PGS000037",
        "trait": "Сахарный диабет 2 типа (15 SNP)",
        "trait_en": "Type 2 diabetes",
        "variants_count": 15,
    },
    {
        "pgs_id": "PGS002247",
        "trait": "Сахарный диабет 2 типа (68 SNP)",
        "trait_en": "Type 2 diabetes",
        "variants_count": 68,
    },
    {
        "pgs_id": "PGS000043",
        "trait": "Сахарный диабет 2 типа (297 SNP)",
        "trait_en": "Type 2 diabetes",
        "variants_count": 297,
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


def calculate_pgs(
    variants_df: pd.DataFrame,
    scoring_df: pd.DataFrame,
) -> dict:
    """Рассчитывает полигенный скор с mean imputation для пропущенных SNP.

    Алгоритм:
      1. Для каждого SNP в scoring-файле:
         а) Если SNP найден в VCF пациента → используем реальную
            дозировку (0, 1 или 2 копии эффект-аллеля).
         б) Если SNP отсутствует, но в scoring-файле есть EAF →
            используем среднюю дозировку 2*EAF (mean imputation).
            Это статистически корректный приём: вместо того чтобы
            выкидывать SNP (что искажает score), мы предполагаем
            "типичный для популяции" генотип у пациента.
         в) Если нет ни генотипа, ни EAF → пропускаем.
      2. PGS = sum(weight * dosage)
      3. Через EAF считаем популяционные mean и variance
         → z-score → перцентиль.

    Свойства mean imputation:
      - При высоком измеренном покрытии (50%+) z-score близок к истинному.
      - При низком покрытии перцентиль автоматически сдвигается к 50-му,
        отражая возросшую неопределённость (это честное поведение).
      - Импутированные SNP не добавляют индивидуального сигнала, только
        корректируют общее среднее и дисперсию.
    """
    rsid_col = "hm_rsID" if "hm_rsID" in scoring_df.columns else "rsID"
    if rsid_col not in scoring_df.columns:
        return {
            "matched": 0, "imputed": 0, "skipped": 0, "total": 0,
            "score": 0.0, "coverage_pct": 0, "effective_coverage_pct": 0,
            "z_score": None, "percentile": None,
        }

    eaf_col = "allelefrequency_effect"
    has_eaf = eaf_col in scoring_df.columns

    vcf_lookup = {}
    for _, row in variants_df.iterrows():
        vcf_lookup[row["rsid"]] = (row["allele_1"], row["allele_2"])

    total_snps = len(scoring_df)
    matched = 0   # SNP реально измерен у пациента
    imputed = 0   # SNP не измерен, но подставлено среднее по популяции
    skipped = 0   # SNP не измерен и нет EAF — нельзя ничего сказать
    score = 0.0
    partial_mean = 0.0
    partial_var = 0.0

    for _, pgs_row in scoring_df.iterrows():
        rsid = pgs_row.get(rsid_col, "")
        if pd.isna(rsid):
            skipped += 1
            continue

        effect_allele = str(pgs_row.get("effect_allele", ""))
        weight = pgs_row.get("effect_weight", 0.0)
        if pd.isna(weight):
            skipped += 1
            continue
        w = float(weight)

        # Достаём популяционную частоту эффект-аллеля для этого SNP
        eaf_raw = pgs_row.get(eaf_col) if has_eaf else None
        eaf_valid = (
            eaf_raw is not None
            and not pd.isna(eaf_raw)
            and 0 < float(eaf_raw) < 1
        )
        eaf = float(eaf_raw) if eaf_valid else None

        if rsid in vcf_lookup:
            # SNP измерен у пациента — реальная дозировка
            a1, a2 = vcf_lookup[rsid]
            dosage = (1 if a1 == effect_allele else 0) + (1 if a2 == effect_allele else 0)
            score += w * dosage
            matched += 1

            # Вклад в популяционные mean/var (для z-score, по Hardy-Weinberg):
            #   E[w*D] = w * 2 * EAF
            #   Var[w*D] = w² * 2 * EAF * (1-EAF)
            if eaf_valid:
                partial_mean += w * 2 * eaf
                partial_var += w ** 2 * 2 * eaf * (1 - eaf)
        elif eaf_valid:
            # SNP не измерен, но известна EAF → mean imputation.
            # Подставляем ожидаемое значение дозировки = 2*EAF.
            # Score сдвигается на w*2*EAF, но (score - mean) от этого SNP = 0,
            # т.е. он не вносит индивидуального вклада в z-score —
            # только в общую дисперсию (увеличивает знаменатель).
            score += w * 2 * eaf
            partial_mean += w * 2 * eaf
            partial_var += w ** 2 * 2 * eaf * (1 - eaf)
            imputed += 1
        else:
            # Нет ни генотипа, ни популяционной частоты — пропускаем
            skipped += 1

    z_score = None
    percentile = None
    if partial_var > 0:
        z_score = round((score - partial_mean) / math.sqrt(partial_var), 2)
        percentile = round(_norm_cdf(z_score) * 100, 1)

    raw_cov = round(matched / total_snps * 100, 1) if total_snps > 0 else 0
    eff_cov = round((matched + imputed) / total_snps * 100, 1) if total_snps > 0 else 0

    return {
        "matched": matched,
        "imputed": imputed,
        "skipped": skipped,
        "total": total_snps,
        "score": round(score, 6),
        "coverage_pct": raw_cov,           # % реально измеренных SNP
        "effective_coverage_pct": eff_cov, # % использованных (measured + imputed)
        "z_score": z_score,
        "percentile": percentile,
    }


def compute_pgs_scores(
    variants_df: pd.DataFrame,
    pgs_list: list[dict] | None = None,
) -> list[dict]:
    """Рассчитывает полигенные скоры для набора заболеваний из PGS Catalog."""
    if pgs_list is None:
        pgs_list = DEFAULT_PGS_SCORES

    print(f"[Стадия 5] Расчёт полигенных шкал риска ({len(pgs_list)} скоров)...")

    results = []
    for pgs_info in pgs_list:
        pgs_id = pgs_info["pgs_id"]
        trait = pgs_info["trait"]

        scoring_df = download_pgs_scoring_file(pgs_id)
        if scoring_df is None:
            print(f"    {pgs_id} ({trait}): не удалось загрузить")
            continue

        calc = calculate_pgs(variants_df, scoring_df)

        # Надёжность судим по реальному покрытию (matched), а не по effective:
        # mean imputation помогает математически, но не заменяет настоящих данных.
        coverage_label, is_reliable = _coverage_label(calc["coverage_pct"])
        risk_level = None
        risk_indicator = None
        if calc["percentile"] is not None:
            risk_level, risk_indicator = _risk_tier(calc["percentile"])

        results.append({
            "pgs_id": pgs_id,
            "trait": trait,
            "trait_en": pgs_info.get("trait_en", ""),
            "score": calc["score"],
            "matched": calc["matched"],
            "imputed": calc["imputed"],
            "skipped": calc["skipped"],
            "total": calc["total"],
            "coverage_pct": calc["coverage_pct"],
            "effective_coverage_pct": calc["effective_coverage_pct"],
            "coverage_label": coverage_label,
            "is_reliable": is_reliable,
            "z_score": calc["z_score"],
            "percentile": calc["percentile"],
            "risk_level": risk_level,
            "risk_indicator": risk_indicator,
        })

        if calc["matched"] > 0 or calc["imputed"] > 0:
            status = "OK"
        else:
            status = "нет данных"
        print(
            f"    {pgs_id}: {trait} | "
            f"измерено {calc['matched']}/{calc['total']} "
            f"({calc['coverage_pct']}%), импутировано {calc['imputed']} | "
            f"score={calc['score']} [{status}]"
        )

    print(f"           Рассчитано скоров: {len(results)}")
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
    print("    ГЕНЕТИЧЕСКИЙ ПРОФИЛЬ: АНАЛИЗ РИСКОВ ЗАБОЛЕВАНИЙ")
    print("=" * 70)

    # --- Сводка ---
    total = len(variants_df)
    mutated = len(variants_df[variants_df["zygosity"] != "homozygous_ref"])
    print(f"\nВсего вариантов в профиле: {total}")
    print(f"Вариантов с мутациями:    {mutated}")

    # --- Раздел 1: Клинически значимые варианты ---
    print("\n" + "-" * 70)
    print("  1. КЛИНИЧЕСКИ ЗНАЧИМЫЕ ВАРИАНТЫ (ClinVar)")
    print("-" * 70)

    if clinvar_df.empty:
        print("  Клинически значимых вариантов не найдено.")
    else:
        # Группируем по уровню значимости (регистронезависимо, без дублей)
        seen_categories = set()
        for significance in ["Pathogenic", "Likely pathogenic",
                             "Pathogenic/Likely pathogenic",
                             "Risk factor",
                             "Drug response",
                             "Association", "Affects"]:
            if significance.lower() in seen_categories:
                continue
            seen_categories.add(significance.lower())
            subset = clinvar_df[
                clinvar_df["significance"].str.contains(significance, case=False, na=False)
            ]
            if subset.empty:
                continue

            print(f"\n  [{significance.upper()}]")
            table_data = []
            for _, row in subset.iterrows():
                cadd = f"CADD:{row['cadd_phred']}" if row["cadd_phred"] else ""
                table_data.append([
                    row["rsid"],
                    row["gene"],
                    row["genotype"],
                    row["zygosity"],
                    row["condition"][:50],
                    cadd,
                ])
            print(tabulate(
                table_data,
                headers=["rsID", "Ген", "Генотип", "Зиготность", "Заболевание", "CADD"],
                tablefmt="simple",
                numalign="left",
            ))

    # --- Раздел 2: Комплексные генотипы ---
    print("\n" + "-" * 70)
    print("  2. КОМПЛЕКСНЫЕ ГЕНОТИПЫ")
    print("-" * 70)

    if not complex_results:
        print("  Известные комплексные генотипы не обнаружены в профиле.")
    else:
        for r in complex_results:
            risk_emoji = {
                "Высокий": "▲▲▲",
                "Повышенный": "▲▲",
                "Умеренно повышенный": "▲",
                "Умеренный": "▲",
                "Носитель": "⚬",
                "Средний": "—",
                "Базовый (средний)": "—",
                "Базовый": "—",
                "Пониженный": "▽",
                "Очень пониженный": "▽▽",
            }.get(r["risk_level"], "?")

            print(f"\n  {r['gene']}: {r['genotype']}")
            print(f"    Заболевание:  {r['disease']}")
            print(f"    Уровень риска: {risk_emoji} {r['risk_level']}")
            print(f"    Подробности:  {r['details']}")

    # --- Раздел 3: Полигенные шкалы риска ---
    print("\n" + "-" * 70)
    print("  3. ПОЛИГЕННЫЕ ШКАЛЫ РИСКА (PGS Catalog)")
    print("-" * 70)

    if not pgs_results:
        print("  Полигенные скоры не рассчитаны.")
    else:
        scored = [r for r in pgs_results if (r["matched"] + r["imputed"]) > 0]
        not_scored = [r for r in pgs_results if (r["matched"] + r["imputed"]) == 0]

        if scored:
            table_data = []
            for r in scored:
                if r["percentile"] is not None and r["is_reliable"]:
                    percentile_str = f"{r['percentile']:.1f}-й"
                    risk_str = f"{r['risk_indicator']} {r['risk_level']}"
                elif r["percentile"] is not None:
                    percentile_str = f"{r['percentile']:.1f}-й *"
                    risk_str = f"{r['risk_indicator']} {r['risk_level']} *"
                else:
                    percentile_str = "—"
                    risk_str = "нет EAF данных"

                # "Измерено / Импутировано / Всего"
                snp_str = f"{r['matched']} / {r['imputed']} / {r['total']}"
                coverage_str = f"{r['coverage_pct']}%"

                table_data.append([
                    r["pgs_id"],
                    r["trait"],
                    f"{r['score']:+.4f}",
                    snp_str,
                    coverage_str,
                    percentile_str,
                    risk_str,
                ])
            print()
            print(tabulate(
                table_data,
                headers=["PGS ID", "Заболевание", "Скор",
                         "Измер./Имп./Всего", "Изм. покрытие",
                         "Перцентиль", "Уровень риска"],
                tablefmt="simple",
                numalign="left",
            ))

            print("\n  Как читать:")
            print("    Измер.     — SNP реально прочитаны на чипе у пациента.")
            print("    Имп.       — SNP отсутствуют в VCF; подставлена средняя")
            print("                 для популяции дозировка (mean imputation).")
            print("                 Эти SNP не добавляют индивидуального сигнала,")
            print("                 но корректируют общую дисперсию.")
            print("    Перцентиль — место пациента в популяции по данному скору.")
            print("                 Например, 80-й = риск выше, чем у 80% людей.")
            print("    * — измеренное покрытие < 50%, интерпретировать осторожно.")

        if not_scored:
            print(f"\n  Нет данных (ни измеренных SNP, ни популяционных частот) для: "
                  f"{', '.join(r['trait'] for r in not_scored)}")

        low_coverage = [r for r in scored if not r["is_reliable"]]
        if low_coverage:
            print(f"\n  ВНИМАНИЕ: измеренное покрытие < 50% для "
                  f"{len(low_coverage)} скор(ов).")
            print("  Mean imputation смягчает пропуски, но при низком измеренном")
            print("  покрытии перцентиль смещён к 50-му (медиане популяции).")
            print("  Для точного результата нужна настоящая импутация по")
            print("  референсной панели (1000G/TOPMed) или WGS.")


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
    annotations = annotate_variants(variants_df)

    # Стадия 3: Извлечение ClinVar
    clinvar_df = extract_clinvar_significance(annotations, variants_df)

    # Стадия 4: Комплексные генотипы
    complex_results = evaluate_complex_genotypes(variants_df)

    # Стадия 5: Полигенные шкалы риска
    pgs_results = compute_pgs_scores(variants_df)

    # Стадия 6: Отчёт
    print_report(variants_df, clinvar_df, complex_results, pgs_results)


if __name__ == "__main__":
    main()
