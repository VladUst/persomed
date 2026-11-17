"""Краткая проверяемая сводка после полного генетического отчёта."""

from pathlib import Path

import pandas as pd
import yaml

from .pgs_catalog import DEFAULT_PGS_SCORES


RULES_FILE = Path(__file__).parent / "resources" / "gene_rules.yaml"


def _clinical_rules() -> dict:
    with RULES_FILE.open(encoding="utf-8") as source:
        return yaml.safe_load(source)


def _exact_variant(row: dict, rule: dict) -> bool:
    return (
        str(row["chrom"]).removeprefix("chr") == rule["chrom"]
        and int(row["pos"]) == rule["pos"]
        and row["ref"] == rule["ref"]
        and row["alt"] == rule["alt"]
        and rule["alt"] in {row["allele_1"], row["allele_2"]}
    )


def _matching_case(rule: dict, observed: dict) -> dict | None:
    return next(
        (case for case in rule["cases"]
         if all(observed.get(key) == value for key, value in case["when"].items())),
        None,
    )


def _findings(
    variants_df: pd.DataFrame, clinvar_df: pd.DataFrame,
    complex_results: list[dict], rules: dict,
) -> tuple[list[dict], set[str]]:
    variant_rules = [rule for rule in rules["findings"] if rule["match"]["type"] == "clinvar"]
    rsids = {rule["match"]["rsid"] for rule in variant_rules}
    lookup = {}
    for row in variants_df[variants_df["rsid"].isin(rsids)].to_dict("records"):
        lookup.setdefault(row["rsid"], []).append(row)

    by_id = {item["id"]: item for item in complex_results}
    findings = []
    summarized_variants = set()
    for rule in rules["findings"]:
        match = rule["match"]
        details = {}
        if match["type"] == "clinvar":
            matches = [row for row in lookup.get(match["rsid"], []) if _exact_variant(row, match)]
            if len(matches) != 1:
                continue
            row = matches[0]
            variant_id = f"chr{match['chrom']}:g.{match['pos']}{match['ref']}>{match['alt']}"
            records = (
                clinvar_df[(clinvar_df["variant"] == variant_id)
                           & (clinvar_df["clinvar_id"] == match["clinvar_id"])
                           & (clinvar_df["category"] == match["category"])]
                if not clinvar_df.empty else pd.DataFrame()
            )
            if records.empty:
                continue
            record = records.iloc[0]
            observed = {"alt_copies": int(row["allele_1"] == match["alt"])
                        + int(row["allele_2"] == match["alt"])}
            details = {
                "rsid": match["rsid"],
                "genotype": f"{row['allele_1']}/{row['allele_2']}",
                "clinvar_id": match["clinvar_id"],
                "clinvar_review_status": record.get("review_status", ""),
                "clinvar_last_evaluated": record.get("last_evaluated", ""),
            }
        elif match["type"] == "genotype_rules":
            rule_ids = match["rule_ids"]
            matched = {rule_id: by_id.get(rule_id) for rule_id in rule_ids}
            if any(item is None or item["status"] == "not_evaluated"
                   for item in matched.values()):
                continue
            observed = {rule_id: item["risk_code"] for rule_id, item in matched.items()}
            details = {
                "rsid": " / ".join(item["rsids"][0] for item in matched.values()),
                "genotype": "; ".join(f"{item['gene']} {item['genotype']}"
                                      for item in matched.values()),
                "rule_ids": rule_ids,
            }
        else:
            raise ValueError(f"Неизвестный тип правила находки: {match['type']}")

        case = _matching_case(rule, observed)
        if case is None:
            continue
        findings.append({
            "id": rule["id"], "gene": rule["gene"], "condition": rule["condition"],
            "role": case["role"], "interpretation": case["interpretation"],
            "recommendation": case["recommendation"], "sources": rule["sources"],
            **details,
        })
        if match["type"] == "clinvar":
            summarized_variants.add(variant_id)
        elif not clinvar_df.empty:
            matched_rsids = {item["rsids"][0] for item in matched.values()}
            summarized_variants.update(
                clinvar_df.loc[clinvar_df["rsid"].isin(matched_rsids), "variant"]
            )
    return findings, summarized_variants


PGS_GROUPS = {
    "Alzheimer's disease": "Болезнь Альцгеймера",
    "Coronary heart disease": "Ишемическая болезнь сердца",
    "Coronary artery disease": "Ишемическая болезнь сердца",
    "Type 2 diabetes": "Диабет 2 типа", "Asthma": "Астма", "Migraine": "Мигрень",
    "Obesity": "Ожирение", "Triglycerides": "Уровень триглицеридов",
}


def _pgs_group(result: dict) -> str:
    model = next(model for model in DEFAULT_PGS_SCORES if model["pgs_id"] == result["pgs_id"])
    return PGS_GROUPS[model["trait_en"]]


def build_clinical_summary(
    variants_df: pd.DataFrame,
    clinvar_df: pd.DataFrame,
    complex_results: list[dict],
    pgs_results: list[dict],
) -> dict:
    """Отбирает точные находки и отделяет их от технических PGS и пропусков."""
    rules = _clinical_rules()
    findings, summarized_variants = _findings(variants_df, clinvar_df, complex_results, rules)

    candidate_variants = (
        set(clinvar_df.loc[clinvar_df["category"] == "candidate", "variant"])
        if not clinvar_df.empty else set()
    )
    remaining_candidates = len(candidate_variants - summarized_variants)

    pgs_by_group = {}
    for result in pgs_results:
        group = _pgs_group(result)
        # Для ИБС PGS000010 имеет опубликованную оценку впервые возникшей
        # болезни в EUR; PGS004321 изучалась для событий в FOURIER.
        model_priority = 1 if result.get("pgs_id") == "PGS000010" else 0
        priority = (
            "eur_percentile" in result,
            model_priority,
            result.get("eur_quality") == "good",
            result.get("coverage_pct", 0),
        )
        previous = pgs_by_group.get(group)
        if previous is None or priority > previous[0]:
            pgs_by_group[group] = (priority, result)

    return {
        "reviewed": rules["reviewed"],
        "findings": findings,
        "other_candidates": remaining_candidates,
        "pgs": [(group, value[1]) for group, value in pgs_by_group.items()],
    }
