"""Синтетические примеры контракта; числа не относятся к реальному пациенту."""

from datetime import datetime, timezone
from uuid import UUID

import pandas as pd

from src.schemas.gene_analysis import Profile
from src.services.gene_analysis.genotype_rules import evaluate_complex_genotypes, load_rules
from src.services.gene_analysis.pgs_catalog import DEFAULT_PGS_SCORES
from src.services.gene_analysis.report import build_report, issue
from src.services.gene_analysis.types import ParsedProfile


def example_report(partial: bool = False):
    variants = []
    for rule in load_rules():
        ids = rule.get("required_snps", [rule.get("snp")])
        for rsid in ids:
            ref, alt = ("T", "C") if rule["type"] == "haplotype" else (
                "A" if rule["risk_allele"] != "A" else "G", rule["risk_allele"])
            if rsid == "rs7412":
                ref, alt = "C", "T"
            variants.append({"chrom": "1", "pos": 100 + len(variants), "rsid": rsid,
                             "ref": ref, "alt": alt, "genotype": "0/0", "allele_1": ref,
                             "allele_2": ref, "zygosity": "homozygous_ref", "phased": False, "phase_set": None})
    variants.append({"chrom": "11", "pos": 71152447, "rsid": "rs11555217", "ref": "C", "alt": "T",
                     "genotype": "0/1", "allele_1": "C", "allele_2": "T", "zygosity": "heterozygous",
                     "phased": False, "phase_set": None})
    frame = pd.DataFrame(variants)
    clinvar = pd.DataFrame([{
        "rsid": "rs11555217", "variant": "chr11:g.71152447C>T", "clinvar_id": "RCV000020436",
        "gene": "DHCR7", "significance": "pathogenic", "category": "candidate",
        "condition": "Синдром Смита — Лемли — Опитца", "genotype": "C/T", "zygosity": "heterozygous",
        "review_status": "criteria provided, single submitter", "last_evaluated": "2026-01-01",
    }])
    scores = []
    for model in DEFAULT_PGS_SCORES:
        count = model["variants_count"]
        scores.append({**model, "status": "research_score", "reason_code": "uncalibrated_score",
                       "reason": "Исследовательская сумма весов", "score": 0.5,
                       "total": count, "matched": count, "imputed": 0, "skipped": 0,
                       "coverage_pct": 100., "effective_coverage_pct": 100., "eur_percentile": 50.,
                       "eur_tier": "average", "eur_z": 0., "eur_r2": 1., "eur_tier_agreement": 1.,
                       "eur_percentile_interval": (50., 50.), "eur_quality": "good", "eur_samples": 503,
                       "eur_reference_snps": count, "eur_matched_snps": count})
    profile = Profile(id=UUID(int=1), filename="synthetic.vcf", size_bytes=1000, sha256="0" * 64,
                      uploaded_at=datetime(2026, 1, 1, tzinfo=timezone.utc), sample_name="SYNTHETIC",
                      build_source="declared")
    report = build_report(1, profile, ParsedProfile(frame, "SYNTHETIC", "declared", len(frame), 0),
                          pd.DataFrame() if partial else clinvar, evaluate_complex_genotypes(frame), scores,
                          issue("annotation_unavailable", "MyVariant.info недоступен; ClinVar не оценён.") if partial else None, [])
    report.generated_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    report.limitations.insert(0, "Демонстрационные синтетические данные; не результат анализа пациента.")
    return report
