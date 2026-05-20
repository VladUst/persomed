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
# Стадия 4: Комплексные генотипы (APOE и др.)
# ---------------------------------------------------------------------------

# Правила для комплексных генотипов, определяемых комбинацией SNP.
# Каждое правило содержит:
#   - name: название генотипа/гена
#   - snps: список rsID, участвующих в определении
#   - rules: функция, принимающая dict{rsid -> (allele1, allele2)} и возвращающая описание

COMPLEX_GENOTYPE_RULES = []


def _apoe_rule(genotypes: dict) -> dict | None:
    """Определяет APOE-генотип по rs429358 и rs7412.

    APOE аллели:
      e2 = rs429358-T + rs7412-T
      e3 = rs429358-T + rs7412-C
      e4 = rs429358-C + rs7412-C
    """
    rs429358 = genotypes.get("rs429358")
    rs7412 = genotypes.get("rs7412")

    if rs429358 is None or rs7412 is None:
        return None

    # Определяем аллели APOE на каждой хромосоме
    # rs429358: REF=T, ALT=C; rs7412: REF=C, ALT=T
    def _classify_haplotype(rs429358_allele: str, rs7412_allele: str) -> str:
        if rs429358_allele == "T" and rs7412_allele == "T":
            return "e2"
        elif rs429358_allele == "T" and rs7412_allele == "C":
            return "e3"
        elif rs429358_allele == "C" and rs7412_allele == "C":
            return "e4"
        elif rs429358_allele == "C" and rs7412_allele == "T":
            # Редкая комбинация (e1), на практике почти не встречается
            return "e1"
        return "?"

    a1_429, a2_429 = rs429358
    a1_7412, a2_7412 = rs7412

    hap1 = _classify_haplotype(a1_429, a1_7412)
    hap2 = _classify_haplotype(a2_429, a2_7412)

    # Сортируем для единообразия (e2/e4, а не e4/e2)
    apoe_genotype = "/".join(sorted([hap1, hap2]))

    # Оценка риска Альцгеймера
    risk_map = {
        "e2/e2": ("Пониженный", "OR ≈ 0.6"),
        "e2/e3": ("Пониженный", "OR ≈ 0.6"),
        "e2/e4": ("Средний", "OR ≈ 2.6"),
        "e3/e3": ("Базовый (средний)", "OR = 1.0"),
        "e3/e4": ("Повышенный", "OR ≈ 3.2"),
        "e4/e4": ("Высокий", "OR ≈ 11.6"),
    }

    risk_level, odds_ratio = risk_map.get(apoe_genotype, ("Неизвестный", "—"))

    return {
        "gene": "APOE",
        "genotype": apoe_genotype,
        "disease": "Болезнь Альцгеймера",
        "risk_level": risk_level,
        "details": f"{odds_ratio}",
    }


COMPLEX_GENOTYPE_RULES.append({
    "name": "APOE (Alzheimer's disease)",
    "snps": ["rs429358", "rs7412"],
    "evaluate": _apoe_rule,
})


def _mthfr_rule(genotypes: dict) -> dict | None:
    """Определяет статус MTHFR по rs1801133 (C677T) и rs1801131 (A1298C)."""
    rs1801133 = genotypes.get("rs1801133")
    rs1801131 = genotypes.get("rs1801131")

    results = []

    if rs1801133 is not None:
        a1, a2 = rs1801133
        if a1 == a2 and a1 != "C":  # Гомозигота TT
            risk = "Значительно сниженная активность MTHFR (~30%)"
            level = "Повышенный"
        elif a1 != a2:  # Гетерозигота CT
            risk = "Умеренно сниженная активность MTHFR (~65%)"
            level = "Умеренный"
        else:
            risk = "Нормальная активность MTHFR"
            level = "Базовый"

        return {
            "gene": "MTHFR (C677T)",
            "genotype": f"{a1}/{a2}",
            "disease": "Гипергомоцистеинемия, дефекты нервной трубки",
            "risk_level": level,
            "details": risk,
        }

    return None


COMPLEX_GENOTYPE_RULES.append({
    "name": "MTHFR C677T",
    "snps": ["rs1801133"],
    "evaluate": _mthfr_rule,
})


def _factor_v_leiden_rule(genotypes: dict) -> dict | None:
    """Фактор V Лейдена (rs6025) — риск тромбозов."""
    rs6025 = genotypes.get("rs6025")
    if rs6025 is None:
        return None

    a1, a2 = rs6025
    if a1 == a2 and a1 != "C":  # Гомозигота по мутации
        return {
            "gene": "F5 (Factor V Leiden)",
            "genotype": f"{a1}/{a2}",
            "disease": "Тромбофилия (венозные тромбозы)",
            "risk_level": "Высокий",
            "details": "Гомозигота — OR ≈ 50-80 для венозной тромбоэмболии",
        }
    elif a1 != a2:  # Гетерозигота
        return {
            "gene": "F5 (Factor V Leiden)",
            "genotype": f"{a1}/{a2}",
            "disease": "Тромбофилия (венозные тромбозы)",
            "risk_level": "Умеренно повышенный",
            "details": "Гетерозигота — OR ≈ 5-7 для венозной тромбоэмболии",
        }
    return None


COMPLEX_GENOTYPE_RULES.append({
    "name": "Factor V Leiden",
    "snps": ["rs6025"],
    "evaluate": _factor_v_leiden_rule,
})


def evaluate_complex_genotypes(variants_df: pd.DataFrame) -> list[dict]:
    """Проверяет все правила комплексных генотипов."""
    results = []

    # Собираем lookup: rsid -> (allele_1, allele_2)
    genotype_lookup = {}
    for _, row in variants_df.iterrows():
        genotype_lookup[row["rsid"]] = (row["allele_1"], row["allele_2"])

    for rule in COMPLEX_GENOTYPE_RULES:
        # Проверяем, есть ли все нужные SNP
        required_snps = rule["snps"]
        available = {s for s in required_snps if s in genotype_lookup}

        if not available:
            continue

        # Передаём доступные генотипы в функцию оценки
        relevant_genotypes = {s: genotype_lookup[s] for s in available}
        result = rule["evaluate"](relevant_genotypes)
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
# Выбраны скоры с небольшим числом вариантов (десятки-сотни) для демонстрации.
# Для продакшена можно добавить скоры с миллионами вариантов (genome-wide PGS).
DEFAULT_PGS_SCORES = [
    {
        "pgs_id": "PGS000010",
        "trait": "Ишемическая болезнь сердца (ИБС)",
        "trait_en": "Coronary heart disease",
        "variants_count": 27,
    },
    {
        "pgs_id": "PGS000011",
        "trait": "Ишемическая болезнь сердца (расш.)",
        "trait_en": "Coronary artery disease",
        "variants_count": 50,
    },
    {
        "pgs_id": "PGS000025",
        "trait": "Болезнь Альцгеймера",
        "trait_en": "Alzheimer's disease",
        "variants_count": 19,
    },
    {
        "pgs_id": "PGS000026",
        "trait": "Болезнь Альцгеймера (расш.)",
        "trait_en": "Alzheimer's disease",
        "variants_count": 33,
    },
    {
        "pgs_id": "PGS000031",
        "trait": "Сахарный диабет 2 типа",
        "trait_en": "Type 2 diabetes",
        "variants_count": 62,
    },
    {
        "pgs_id": "PGS000001",
        "trait": "Рак молочной железы",
        "trait_en": "Breast cancer",
        "variants_count": 77,
    },
    {
        "pgs_id": "PGS000019",
        "trait": "Ишемическая болезнь сердца (192 SNP)",
        "trait_en": "Coronary artery disease",
        "variants_count": 192,
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
    """Рассчитывает полигенный скор для одного PGS scoring-файла.

    Алгоритм:
      1. Для каждого SNP в scoring-файле ищем совпадение по rsID в VCF
      2. Считаем дозировку эффект-аллеля (0, 1 или 2 копии)
      3. PGS = sum(effect_weight * dosage)
      4. Если в файле есть частоты аллелей (allelefrequency_effect),
         вычисляем среднее и СКО для найденных SNP → z-score → перцентиль.

    Возвращает dict с результатами.
    """
    rsid_col = "hm_rsID" if "hm_rsID" in scoring_df.columns else "rsID"
    if rsid_col not in scoring_df.columns:
        return {"matched": 0, "total": 0, "score": 0.0, "coverage_pct": 0,
                "z_score": None, "percentile": None}

    eaf_col = "allelefrequency_effect"
    has_eaf = eaf_col in scoring_df.columns

    vcf_lookup = {}
    for _, row in variants_df.iterrows():
        vcf_lookup[row["rsid"]] = (row["allele_1"], row["allele_2"])

    total_snps = len(scoring_df)
    matched = 0
    score = 0.0
    # Для вычисления z-score: среднее и дисперсия по найденным SNP
    partial_mean = 0.0
    partial_var = 0.0
    eaf_used = 0

    for _, pgs_row in scoring_df.iterrows():
        rsid = pgs_row.get(rsid_col, "")
        if pd.isna(rsid) or rsid not in vcf_lookup:
            continue

        effect_allele = str(pgs_row.get("effect_allele", ""))
        weight = pgs_row.get("effect_weight", 0.0)
        if pd.isna(weight):
            continue

        a1, a2 = vcf_lookup[rsid]
        dosage = (1 if a1 == effect_allele else 0) + (1 if a2 == effect_allele else 0)
        w = float(weight)

        score += w * dosage
        matched += 1

        # Вклад этого SNP в среднее и дисперсию популяции:
        #   E[w*D] = w * 2 * EAF          (по Hardy-Weinberg)
        #   Var[w*D] = w² * 2 * EAF * (1-EAF)
        if has_eaf:
            eaf = pgs_row.get(eaf_col)
            if eaf is not None and not pd.isna(eaf):
                eaf = float(eaf)
                if 0 < eaf < 1:
                    partial_mean += w * 2 * eaf
                    partial_var += w ** 2 * 2 * eaf * (1 - eaf)
                    eaf_used += 1

    z_score = None
    percentile = None
    if eaf_used > 0 and partial_var > 0:
        z_score = round((score - partial_mean) / math.sqrt(partial_var), 2)
        percentile = round(_norm_cdf(z_score) * 100, 1)

    return {
        "matched": matched,
        "total": total_snps,
        "score": round(score, 6),
        "coverage_pct": round(matched / total_snps * 100, 1) if total_snps > 0 else 0,
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
            "total": calc["total"],
            "coverage_pct": calc["coverage_pct"],
            "coverage_label": coverage_label,
            "is_reliable": is_reliable,
            "z_score": calc["z_score"],
            "percentile": calc["percentile"],
            "risk_level": risk_level,
            "risk_indicator": risk_indicator,
        })

        status = "OK" if calc["matched"] > 0 else "нет совпадений"
        print(
            f"    {pgs_id}: {trait} | "
            f"совпало {calc['matched']}/{calc['total']} SNP "
            f"({calc['coverage_pct']}%) | score={calc['score']} [{status}]"
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
                "Средний": "—",
                "Базовый (средний)": "—",
                "Базовый": "—",
                "Пониженный": "▽",
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
        scored = [r for r in pgs_results if r["matched"] > 0]
        not_scored = [r for r in pgs_results if r["matched"] == 0]

        if scored:
            # Таблица: показываем перцентиль и уровень риска там, где есть данные
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

                table_data.append([
                    r["pgs_id"],
                    r["trait"],
                    f"{r['score']:+.4f}",
                    f"{r['matched']}/{r['total']}",
                    f"{r['coverage_pct']}% ({r['coverage_label']})",
                    percentile_str,
                    risk_str,
                ])
            print()
            print(tabulate(
                table_data,
                headers=["PGS ID", "Заболевание", "Скор", "SNP", "Покрытие", "Перцентиль", "Уровень риска"],
                tablefmt="simple",
                numalign="left",
            ))

            print("\n  Как читать:")
            print("    Перцентиль — место пациента в популяции по данному скору.")
            print("    Например, 80-й перцентиль = генетический риск выше, чем у 80% людей.")
            print("    * — покрытие < 20%, результат предварительный.")

        if not_scored:
            print(f"\n  Нет совпадений SNP для: "
                  f"{', '.join(r['trait'] for r in not_scored)}")

        low_coverage = [r for r in scored if not r["is_reliable"]]
        if low_coverage:
            print(f"\n  ВНИМАНИЕ: Покрытие < 20% для "
                  f"{len(low_coverage)} скор(ов) — для точного расчёта")
            print("  нужен полный SNP-массив (~650k SNP) или WGS.")


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
