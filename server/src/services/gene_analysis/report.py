"""Представление результатов для таблиц и краткой врачебной сводки."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from src.schemas.gene_analysis import GeneAnalysisReport, Profile
from .clinical_summary import build_clinical_summary
from .config import ANALYSIS_VERSION, RESOURCES
from .pgs_catalog import DEFAULT_PGS_SCORES
from .types import ParsedProfile

CATEGORIES = {
    "candidate": "Кандидат для проверки", "conflicting": "Спорное заключение",
    "uncertain": "Неопределённая значимость", "association": "Ассоциация",
    "drug_response": "Фармакогенетика",
}
TIERS = {
    "low": "Пониженное", "moderately_low": "Умеренно пониженное", "average": "Среднее",
    "moderately_high": "Умеренно повышенное", "high": "Повышенное", "very_high": "Очень высокое",
}
TRAITS = {
    "Alzheimer's disease": "alzheimers", "Coronary heart disease": "coronary_disease",
    "Coronary artery disease": "coronary_disease", "Type 2 diabetes": "type_2_diabetes",
    "Asthma": "asthma", "Migraine": "migraine", "Obesity": "obesity", "Triglycerides": "triglycerides",
}
LIMITATIONS = [
    "Отчёт предназначен для экспертного разбора и не устанавливает диагноз.",
    "Перцентиль PGS — положение балла в EUR-референсе, не вероятность заболевания.",
    "Генетическое происхождение пациента и применимость EUR-референса не определялись.",
    "Качество вызовов, глубина покрытия и FILTER автоматически не оценивались.",
    "Отсутствие записи в VCF не означает отсутствие аллеля; охват вариантов и моделей ограничен.",
    "Значимые варианты требуют клинического подтверждения и сопоставления с фенотипом.",
]


def issue(code: str, message: str) -> dict:
    return {"code": code, "message": message}


def reference(section: str, item_id: str) -> dict:
    return {"section": section, "item_id": item_id}


def interval(values: tuple | list) -> dict:
    return {"lower": values[0], "upper": values[1]}


def _clinvar_items(frame: pd.DataFrame, variants: pd.DataFrame) -> list[dict]:
    items = []
    for row in frame.to_dict("records"):
        chromosome, position_and_alleles = row["variant"].split(":g.")
        # Идентификатор уже проверен точным сопоставлением в clinvar.py.
        variant = variants[(variants["rsid"] == row["rsid"]) &
                           (variants["chrom"].astype(str).str.removeprefix("chr") == chromosome.removeprefix("chr")) &
                           (variants["pos"] == int(position_and_alleles[:-3])) &
                           (variants["ref"] == position_and_alleles[-3]) &
                           (variants["alt"] == position_and_alleles[-1])].iloc[0]
        identity = "|".join(str(row[key]) for key in ("variant", "clinvar_id", "significance", "condition"))
        accession = row["clinvar_id"] or None
        evaluated = pd.to_datetime(row["last_evaluated"], errors="coerce")
        items.append({
            "id": hashlib.sha256(identity.encode()).hexdigest()[:24],
            "variant": {"chromosome": chromosome.removeprefix("chr"), "position": int(variant["pos"]),
                        "ref": variant["ref"], "alt": variant["alt"], "rsid": row["rsid"]},
            "genes": [name.strip() for name in row["gene"].split(",") if name.strip()],
            "genotype": row["genotype"], "zygosity": row["zygosity"],
            "conditions": [name.strip() for name in row["condition"].split(";") if name.strip()],
            "category": row["category"],
            "significance": {"original": row["significance"], "label": CATEGORIES[row["category"]]},
            "accession": accession, "review_status": row["review_status"] or None,
            "last_evaluated": None if pd.isna(evaluated) else evaluated.date(),
            "source_url": f"https://www.ncbi.nlm.nih.gov/clinvar/{accession}/" if accession else None,
        })
    return items


def _rule_items(results: list[dict]) -> list[dict]:
    items = []
    for row in results:
        items.append({
            "id": row["id"], "genes": [row["gene"].split()[0]], "condition": row["disease"],
            "status": row["status"],
            "reason": issue(row["reason_code"], row["details"]) if row["reason_code"] else None,
            "observed_variants": [{
                "rsid": observed["rsid"], "genotype": observed["genotype"],
                "alleles": [observed["allele_1"], observed["allele_2"]], "phased": observed["phased"],
                "phase_set": None if pd.isna(observed["phase_set"]) else str(observed["phase_set"]),
            } for observed in row["observed"]],
            "diplotype": row["diplotype"],
            "result": {"code": row["risk_code"], "label": row["risk_level"], "explanation": row["details"]}
                      if row["status"] == "evaluated" else None,
            "effect": {"value": row["effect"], "context": row["disease"], "sources": row["sources"]}
                      if row["effect"] is not None else None,
            "limitations": ["Правило не устанавливает диагноз; OR не является абсолютной вероятностью."],
            "sources": row["sources"],
        })
    return items


def _pgs_items(results: list[dict]) -> list[dict]:
    models = {model["pgs_id"]: model for model in DEFAULT_PGS_SCORES}
    items = []
    for row in results:
        model = models[row["pgs_id"]]
        evaluated = row["status"] != "not_evaluated"
        compared = "eur_percentile" in row
        coverage = None
        if "total" in row:
            coverage = {key: row[key] for key in ("total", "matched", "imputed", "skipped")}
            coverage.update(measured_percent=row["coverage_pct"], effective_percent=row["effective_coverage_pct"])
        items.append({
            "pgs_id": row["pgs_id"], "trait_id": TRAITS[model["trait_en"]], "trait": model["trait"],
            "source_url": model.get("source", f"https://www.pgscatalog.org/score/{row['pgs_id']}/"),
            "status": "evaluated" if evaluated else "not_evaluated",
            "reason": issue(row["reason_code"], row["reason"]), "coverage": coverage,
            "raw_score": row.get("score") if evaluated else None,
            "reference_comparison": {
                "status": "evaluated" if compared else "not_evaluated",
                "reason": None if compared else issue(row.get("eur_reason_code", "reference_unavailable"),
                                                       row.get("eur_reason", "EUR-сравнение недоступно")),
                "sample_count": row.get("eur_samples"), "reference_snps": row.get("eur_reference_snps"),
                "patient_snps": row.get("eur_matched_snps"), "percentile": row.get("eur_percentile"),
                "category": row.get("eur_tier"), "category_label": TIERS.get(row.get("eur_tier")),
                "z_score": row.get("eur_z"),
            },
            "stability": {"quality": row["eur_quality"], "r_squared": row["eur_r2"],
                          "tier_agreement": row["eur_tier_agreement"],
                          "percentile_interval": interval(row["eur_percentile_interval"])} if compared else None,
            "research_effect": {"value": row["eur_relative_hr"], "range": interval(row["eur_relative_hr_range"]),
                                "outcome": row["eur_outcome"], "source_url": row["eur_effect_source"],
                                "note": row["eur_hr_note"]} if "eur_relative_hr" in row else None,
        })
    return items


def _summary(raw: dict, clinvar: list[dict], rules: list[dict], pgs: list[dict], available: bool) -> dict:
    findings = []
    for index, row in enumerate(raw["findings"]):
        refs = []
        if row.get("clinvar_id"):
            refs = [reference("clinvar", item["id"]) for item in clinvar
                    if item["accession"] == row["clinvar_id"] and item["variant"]["rsid"] == row["rsid"]]
        else:
            refs = [reference("genotype_rules", item["id"]) for item in rules if row["gene"] in item["genes"]]
        findings.append({
            "id": row.get("id", f"rule_finding_{index}"), "genes": [row["gene"]],
            **{key: row[key] for key in ("condition", "role", "interpretation", "clinical_question", "next_step")},
            "limitations": [row["limitation"]], "evidence_refs": refs, "sources": [{"url": row["source"]}],
        })
    not_detected = [{"message": f"{', '.join(item['genes'])}: указанный аллель не выявлен",
                     "evidence_refs": [reference("genotype_rules", item["id"])]}
                    for item in rules if item["result"] and item["result"]["code"] == "not_detected"]
    not_evaluated = [{"message": item["reason"]["message"], "evidence_refs": [reference("genotype_rules", item["id"])]}
                     for item in rules if item["status"] == "not_evaluated"]
    for item in pgs:
        reason = item["reason"] if item["status"] == "not_evaluated" else item["reference_comparison"]["reason"]
        if reason:
            not_evaluated.append({"message": f"{item['pgs_id']}: {reason['message']}",
                                  "evidence_refs": [reference("polygenic_scores", item["pgs_id"])]})
    for item in clinvar:
        if item["category"] == "conflicting":
            not_evaluated.append({"message": "Заключения ClinVar конфликтуют; диагноз по маркеру не установлен.",
                                  "evidence_refs": [reference("clinvar", item["id"])]})
    if not available:
        not_evaluated.append({"message": "ClinVar недоступен: отсутствие находок не установлено.", "evidence_refs": []})
    by_id = {item["pgs_id"]: item for item in pgs}
    overview = [{"trait_id": by_id[row["pgs_id"]]["trait_id"], "trait": group, "pgs_id": row["pgs_id"]}
                for group, row in raw["pgs"]]
    return {"findings": findings, "not_detected": not_detected, "not_evaluated": not_evaluated,
            "polygenic_overview": overview, "other_candidate_variants_count": raw["other_candidates"] if available else None}


def build_report(patient_id: int, profile: Profile, parsed: ParsedProfile, clinvar: pd.DataFrame,
                 rules: list[dict], scores: list[dict], annotation_issue: dict | None,
                 resource_paths: list[Path]) -> GeneAnalysisReport:
    """Отделяет вычисления от публичной схемы и проверяет все ссылки сводки."""
    clinical_items = _clinvar_items(clinvar, parsed.variants)
    rule_items = _rule_items(rules)
    pgs_items = _pgs_items(scores)
    raw_summary = build_clinical_summary(parsed.variants, clinvar, rules, scores)
    pgs_partial = any(item["status"] == "not_evaluated" or item["reference_comparison"]["status"] == "not_evaluated"
                      for item in pgs_items)
    rules_partial = any(item["status"] == "not_evaluated" for item in rule_items)
    quality_issues = [issue("quality_not_filtered", "FILTER, глубина и качество вызовов автоматически не проверялись.")]
    if profile.build_source == "assumed":
        quality_issues.append(issue("assumed_grch37", "Сборка не указана: предполагается GRCh37; необходимо проверить происхождение VCF."))
    resources = [*RESOURCES.glob("*.yaml"), *resource_paths]
    return GeneAnalysisReport.model_validate({
        "analysis_version": ANALYSIS_VERSION, "patient_id": patient_id, "profile": profile,
        "generated_at": datetime.now(timezone.utc),
        "status": "partial" if annotation_issue or pgs_partial or rules_partial else "complete",
        "summary": _summary(raw_summary, clinical_items, rule_items, pgs_items, annotation_issue is None),
        "clinvar": {"status": "unavailable" if annotation_issue else "complete",
                    "issues": [annotation_issue] if annotation_issue else [], "items": clinical_items},
        "genotype_rules": {"status": "partial" if rules_partial else "complete", "items": rule_items},
        "polygenic_scores": {"status": "partial" if pgs_partial else "complete", "items": pgs_items},
        "quality": {"total_records": parsed.total_records, "usable_records": len(parsed.variants),
                    "skipped_records": parsed.skipped_records,
                    "alt_records": int((parsed.variants["zygosity"] != "homozygous_ref").sum()),
                    "unmatched_annotations": clinvar.attrs.get("unmatched_annotations", 0), "issues": quality_issues},
        "limitations": LIMITATIONS,
        "provenance": {"rules_reviewed": raw_summary["reviewed"],
                       "resources": [{"name": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                                     for path in resources if path.is_file()],
                       "sources": [{"url": "https://myvariant.info/"}, {"url": "https://www.pgscatalog.org/"},
                                   {"url": "https://www.internationalgenome.org/"}],
                       "annotation_cache_policy": "Ответы MyVariant сохраняются без автоматического срока обновления."},
    })
