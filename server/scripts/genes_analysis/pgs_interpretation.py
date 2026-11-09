"""Сопоставление PGS с индивидуальными EUR-генотипами 1000 Genomes.

Перцентиль — положение генетического балла в референсе, не вероятность болезни.
Численная оценка HR допускается только для выбранного совпадающего исхода.
"""

from pathlib import Path

import numpy as np
import pandas as pd


REFERENCE_FILE = Path(__file__).parent / ".pgs_cache" / "eur_1000g_phase3_grch37.npz"

# PGS000010: впервые возникшая ИБС, европейская выборка, HR на 1 SD.
# PGS Catalog PPM000017 / Tada et al. Eur Heart J (2015).
EFFECTS = {
    "PGS000010": {
        "hr_per_sd": 1.20,
        "hr_ci": (1.15, 1.25),
        "outcome": "впервые возникшая ИБС",
        "source": "https://www.pgscatalog.org/score/PGS000010/",
    },
}


def _tier(percentile: float) -> str:
    """Условная шкала положения PGS среди EUR-образцов, не клинический порог."""
    if percentile >= 95:
        return "очень высокая"
    if percentile >= 80:
        return "повышенная"
    if percentile >= 60:
        return "умеренно повышенная"
    if percentile >= 40:
        return "средняя"
    if percentile >= 20:
        return "умеренно пониженная"
    return "пониженная"


def _ranks(values: np.ndarray) -> np.ndarray:
    return pd.Series(values).rank(method="average", pct=True).to_numpy() * 100


def _percentile(value: float, distribution: np.ndarray) -> float:
    return 100 * (
        np.count_nonzero(distribution < value)
        + 0.5 * np.count_nonzero(distribution == value)
    ) / len(distribution)


def _reference_dosages(
    alleles: np.ndarray, effect: str, other: str | None,
) -> np.ndarray | None:
    """Возвращает дозировки только для однонуклеотидного двуаллельного SNP."""
    if effect not in {"A", "C", "G", "T"}:
        return None
    observed = {base.decode() for base in np.unique(alleles) if base}
    allowed_bases = ({effect, other} if other in {"A", "C", "G", "T"}
                     else observed | {effect})
    if (not observed or len(allowed_bases) != 2
            or not observed.issubset(allowed_bases)):
        return None
    allowed = {base.encode() for base in allowed_bases}
    valid = np.isin(alleles[:, 0], list(allowed)) & np.isin(alleles[:, 1], list(allowed))
    if valid.mean() < 0.95:
        return None
    dosage = (alleles[:, 0] == effect.encode()).astype(float)
    dosage += (alleles[:, 1] == effect.encode()).astype(float)
    dosage[~valid] = np.nan
    dosage[np.isnan(dosage)] = np.nanmean(dosage)
    return dosage


def interpret_pgs(
    variants_df: pd.DataFrame,
    pgs_results: list[dict],
    scoring_loader,
    alleles_match,
    reference_file: Path = REFERENCE_FILE,
) -> list[dict]:
    """Дополняет существующие результаты относительным EUR-перцентилем.

    Для пациента и референса частичный балл использует ровно одинаковые SNP.
    Подстановка EAF из общего расчёта здесь не применяется.
    """
    if not reference_file.exists():
        for result in pgs_results:
            result["eur_reason"] = "EUR-референс не подготовлен"
        return pgs_results

    with np.load(reference_file, allow_pickle=False) as source:
        ref_ids = source["rsids"].tolist()
        ref_chrom = source["chrom"].tolist()
        ref_pos = source["pos"].tolist()
        ref_alleles = source["alleles"]
        sample_count = len(source["samples"])
    ref_index = {rsid: index for index, rsid in enumerate(ref_ids)}
    relevant_ids = set(ref_ids)
    patient_lookup = {}
    for row in variants_df[variants_df["rsid"].isin(relevant_ids)].to_dict("records"):
        patient_lookup.setdefault(row["rsid"], []).append(row)

    for result in pgs_results:
        if result.get("status") == "Не оценено":
            result["eur_reason"] = "Меньше 30% SNP или файл весов недоступен"
            continue
        scoring = scoring_loader(result["pgs_id"])
        if scoring is None:
            result["eur_reason"] = "Файл весов недоступен"
            continue

        full_ref = np.zeros(sample_count)
        partial_ref = np.zeros(sample_count)
        patient_score = 0.0
        reference_snps = 0
        patient_snps = 0
        for _, pgs_row in scoring.iterrows():
            rsid = pgs_row.get("hm_rsID")
            index = ref_index.get(rsid)
            if index is None:
                continue
            chrom = str(pgs_row.get("hm_chr")).removesuffix(".0").removeprefix("chr")
            pos = pgs_row.get("hm_pos")
            if pd.isna(pos) or chrom != str(ref_chrom[index]) or int(pos) != int(ref_pos[index]):
                continue
            effect = str(pgs_row.get("effect_allele", "")).upper()
            other_raw = pgs_row.get("other_allele")
            if other_raw is None or pd.isna(other_raw):
                other_raw = pgs_row.get("hm_inferOtherAllele")
            other = str(other_raw).upper() if other_raw is not None and not pd.isna(other_raw) else None
            weight = pgs_row.get("effect_weight")
            if pd.isna(weight):
                continue
            dosage = _reference_dosages(ref_alleles[index], effect, other)
            if dosage is None:
                continue
            weighted = dosage * float(weight)
            full_ref += weighted
            reference_snps += 1

            matches = [
                row for row in patient_lookup.get(rsid, [])
                if str(row["chrom"]).removeprefix("chr") == chrom
                and int(row["pos"]) == int(pos)
                and alleles_match(pgs_row, row, effect)
            ]
            if len(matches) != 1:
                continue
            row = matches[0]
            patient_score += float(weight) * (
                (row["allele_1"] == effect) + (row["allele_2"] == effect)
            )
            partial_ref += weighted
            patient_snps += 1

        total = len(scoring)
        result["eur_reference_snps"] = reference_snps
        result["eur_matched_snps"] = patient_snps
        result["eur_samples"] = sample_count
        if (reference_snps < 0.9 * total or patient_snps < 0.3 * total
                or np.std(partial_ref) == 0 or np.std(full_ref) == 0):
            result["eur_reason"] = "Недостаточно совпадающих SNP в EUR-референсе"
            continue

        percentile = _percentile(patient_score, partial_ref)
        z_partial = (patient_score - partial_ref.mean()) / partial_ref.std(ddof=1)
        correlation = float(np.corrcoef(full_ref, partial_ref)[0, 1])
        if not np.isfinite(correlation) or correlation <= 0:
            result["eur_reason"] = "Частичный балл не воспроизводит направление полного балла в EUR-референсе"
            continue
        r2 = max(0.0, correlation ** 2)
        full_tiers = [_tier(value) for value in _ranks(full_ref)]
        partial_tiers = [_tier(value) for value in _ranks(partial_ref)]
        agreement = float(np.mean(np.asarray(full_tiers) == np.asarray(partial_tiers)))
        slope = np.cov(full_ref, partial_ref, ddof=1)[0, 1] / np.var(partial_ref, ddof=1)
        predicted_full = full_ref.mean() + slope * (patient_score - partial_ref.mean())
        residuals = full_ref - (full_ref.mean() + slope * (partial_ref - partial_ref.mean()))
        low_residual, high_residual = np.quantile(residuals, [0.05, 0.95])
        full_score_interval = (predicted_full + low_residual,
                               predicted_full + high_residual)
        percentile_interval = tuple(
            round(_percentile(value, full_ref), 1) for value in full_score_interval
        )
        tier_span = {_tier(percentile_interval[0]), _tier(percentile_interval[1])}
        quality = (
            "хорошая" if r2 >= 0.8 and len(tier_span) == 1 else
            "ограниченная" if r2 >= 0.6 else
            "низкая"
        )
        result.update({
            "eur_percentile": round(percentile, 1),
            "eur_tier": _tier(percentile),
            "eur_z": round(float(z_partial), 3),
            "eur_r2": round(r2, 3),
            "eur_tier_agreement": round(agreement, 3),
            "eur_percentile_interval": percentile_interval,
            "eur_quality": quality,
            "eur_reason": "",
        })

        # Перенос опубликованного HR на неполный балл требует особой осторожности.
        # Допускаем только модель с совпадающим исходом и устойчивым рангом.
        effect_info = EFFECTS.get(result["pgs_id"])
        if (effect_info and quality == "хорошая" and reference_snps >= 0.9 * total
                and patient_snps >= 0.7 * total):
            # Линейная проекция полного балла на измеренный; остатки дают
            # ориентировочный диапазон ошибки из-за недоступных SNP пациента.
            estimated_full_z = (predicted_full - full_ref.mean()) / full_ref.std(ddof=1)
            z_bounds = [(value - full_ref.mean()) / full_ref.std(ddof=1)
                        for value in full_score_interval]
            hr = effect_info["hr_per_sd"] ** estimated_full_z
            lower, upper = effect_info["hr_ci"]
            reported_bounds = sorted(base ** z for base in (lower, upper)
                                     for z in z_bounds)
            result.update({
                "eur_relative_hr": round(hr, 2),
                "eur_relative_hr_range": (round(reported_bounds[0], 2),
                                          round(reported_bounds[-1], 2)),
                "eur_outcome": effect_info["outcome"],
                "eur_effect_source": effect_info["source"],
                "eur_hr_note": "Исследовательская экстраполяция HR с полного PGS на частичный. "
                               "SD 1000 Genomes может отличаться от SD исходного исследования. "
                               "Для этого пациента оценка клинически не валидирована; "
                               "диапазон не является клиническим доверительным интервалом.",
            })
    return pgs_results
