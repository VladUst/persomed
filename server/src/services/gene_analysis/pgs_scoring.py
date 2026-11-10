import re
from collections.abc import Callable
import pandas as pd
from .pgs_catalog import DEFAULT_PGS_SCORES, download_pgs_scoring_file


def _coverage_label(coverage_pct: float) -> tuple[str, bool]:
    """Порог отображения исследовательского расчёта, не клинической оценки."""
    if coverage_pct >= 75:
        return "Измерено ≥75% SNP", True
    if coverage_pct >= 30:
        return "Измерено 30–74% SNP", True
    return "Измерено <30% SNP", False


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
    scoring_loader: Callable[[str], pd.DataFrame | None] = download_pgs_scoring_file,
) -> list[dict]:
    """Рассчитывает исследовательские суммы только для простых моделей."""
    if pgs_list is None:
        pgs_list = DEFAULT_PGS_SCORES


    results = []
    for pgs_info in pgs_list:
        pgs_id = pgs_info["pgs_id"]
        trait = pgs_info["trait"]

        scoring_df = scoring_loader(pgs_id)
        if scoring_df is None:
            results.append({"pgs_id": pgs_id, "trait": trait, "status": "not_evaluated",
                            "reason_code": "weights_unavailable", "reason": "Не удалось загрузить файл весов"})
            continue

        required = {"effect_allele", "effect_weight", "hm_chr", "hm_pos"}
        if not required.issubset(scoring_df.columns) or any(
            column.startswith("dosage_") and column.endswith("_weight")
            for column in scoring_df.columns
        ) or len(scoring_df) != pgs_info.get("variants_count"):
            results.append({"pgs_id": pgs_id, "trait": trait, "status": "not_evaluated",
                            "reason_code": "unsupported_weights", "reason": "Формат или размер файла весов не соответствует поддерживаемой модели"})
            continue

        calc = calculate_pgs(variants_df, scoring_df)
        coverage_label, has_minimum_overlap = _coverage_label(calc["coverage_pct"])
        if not has_minimum_overlap:
            status = "not_evaluated"
            reason = "Измерено менее 30% SNP модели"
        elif calc["skipped"]:
            status = "partial_score"
            reason = f"Не учтено {calc['skipped']} SNP; сумма неполная"
        else:
            status = "research_score"
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
            "reason_code": "insufficient_coverage" if not has_minimum_overlap else "partial_score" if calc["skipped"] else "uncalibrated_score",
        })


    return results
