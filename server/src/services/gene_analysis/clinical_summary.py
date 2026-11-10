"""Краткая проверяемая сводка после полного генетического отчёта."""

from pathlib import Path

import pandas as pd
import yaml

from .pgs_catalog import DEFAULT_PGS_SCORES


RULES_FILE = Path(__file__).parent / "resources" / "clinical_findings.yaml"


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
    rsids = {rule["rsid"] for rule in rules["findings"]}
    lookup = {}
    for row in variants_df[variants_df["rsid"].isin(rsids)].to_dict("records"):
        lookup.setdefault(row["rsid"], []).append(row)

    findings = []
    summarized_variants = set()
    for rule in rules["findings"]:
        matching = [row for row in lookup.get(rule["rsid"], []) if _exact_variant(row, rule)]
        if len(matching) != 1:
            continue
        row = matching[0]
        variant_id = f"chr{rule['chrom']}:g.{rule['pos']}{rule['ref']}>{rule['alt']}"
        matching_clinvar = (
            clinvar_df[(clinvar_df["variant"] == variant_id)
                       & (clinvar_df["clinvar_id"] == rule["clinvar_id"])]
            if not clinvar_df.empty else pd.DataFrame()
        )
        if matching_clinvar.empty:
            continue
        clinvar_record = matching_clinvar.iloc[0]
        copies = (row["allele_1"] == rule["alt"]) + (row["allele_2"] == rule["alt"])
        findings.append({
            **rule,
            "variant": variant_id,
            "genotype": f"{row['allele_1']}/{row['allele_2']}",
            "role": rule["two_copies_role"] if copies == 2 else rule["one_copy_role"],
            "clinvar_review_status": clinvar_record.get("review_status", ""),
            "clinvar_last_evaluated": clinvar_record.get("last_evaluated", ""),
        })
        summarized_variants.add(variant_id)

    by_id = {item["id"]: item for item in complex_results}
    h63d = by_id.get("hfe_h63d")
    c282y = by_id.get("hfe_c282y")
    if h63d and c282y and h63d["status"] != "not_evaluated" and c282y["status"] != "not_evaluated":
        if h63d["risk_code"] == "marker" or c282y["risk_code"] in {"carrier", "high"}:
            role = (
                "Генотип, ассоциированный с перегрузкой железом — подтвердить"
                if c282y["risk_code"] == "high" else
                "Маркер HFE; диагноз гемохроматоза не установлен"
            )
            findings.append({
                "id": "hfe_combined", "gene": "HFE", "rsid": "rs1799945 / rs1800562",
                "genotype": f"H63D {h63d['genotype']}; C282Y {c282y['genotype']}",
                "condition": "Перегрузка железом", "role": role,
                "interpretation": "Генотип сопоставляется с показателями обмена железа и фенотипом.",
                "clinical_question": "Есть ли повышение насыщения трансферрина, ферритина или признаки перегрузки железом?",
                "next_step": "Если есть клиническое подозрение, оценить насыщение трансферрина и ферритин по профильным рекомендациям.",
                "limitation": "H63D сам по себе не подтверждает HFE-гемохроматоз.",
                "source": "https://easl.eu/wp-content/uploads/2022/06/PIIS01688278220021121.pdf",
            })
            summarized_variants.add("chr6:g.26091179C>G")

    hla = by_id.get("hla_b5701")
    if hla and hla["risk_code"] == "proxy_marker":
        findings.append({
            "id": "hla_proxy", "gene": "HLA-B", "rsid": "rs2395029", "genotype": hla["genotype"],
            "condition": "Гиперчувствительность к абакавиру",
            "role": "Косвенный лекарственный маркер — требуется типирование",
            "interpretation": "SNP связан с HLA-B*57:01, но не определяет HLA-аллель напрямую.",
            "clinical_question": "Планируется ли назначение абакавира?",
            "next_step": "Перед назначением получить прямой результат HLA-B*57:01-типирования.",
            "limitation": "По tag SNP нельзя назначать или отменять лекарство.",
            "source": "https://cpicpgx.org/wp-content/uploads/2016/01/CPIC_HLAB-Abacavir.pdf",
        })

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
