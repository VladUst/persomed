"""Конвейер анализа и повторное использование неизменяемого отчёта."""

from zipfile import BadZipFile

import pandas as pd

from src.schemas.gene_analysis import GeneAnalysisReport
from .annotations import AnnotationError, annotate_variants
from .clinvar import extract_clinvar_significance
from .cache_import import validate_reference
from .errors import GeneAnalysisError
from .genotype_rules import evaluate_complex_genotypes
from .pgs_catalog import download_pgs_scoring_file
from .pgs_interpretation import interpret_pgs
from .pgs_scoring import _pgs_alleles_match, compute_pgs_scores
from .profile_storage import ProfileStorage
from .report import build_report, issue
from .vcf_parser import parse_vcf


def analyze_profile(patient_id: int, storage: ProfileStorage) -> GeneAnalysisReport:
    """Вызывается под блокировкой пациента в рабочем потоке, не в event loop."""
    profile = storage.current(patient_id)
    if profile is None:
        raise GeneAnalysisError("Генетический профиль ещё не загружен.", 404)
    cached = storage.read_report(patient_id, profile)
    if cached is not None:
        return cached
    path = storage.profile_dir(patient_id, profile) / "profile.vcf"
    if not path.is_file():
        raise GeneAnalysisError("Файл профиля отсутствует; загрузите его повторно.", 409)
    parsed = parse_vcf(path)
    annotation_issue = None
    try:
        annotations = annotate_variants(parsed.variants, cache_dir=storage.root / "cache" / "myvariant")
        clinvar = extract_clinvar_significance(annotations, parsed.variants)
    except AnnotationError:
        annotation_issue = issue("annotation_unavailable", "MyVariant.info недоступен; раздел ClinVar не оценён.")
        clinvar = pd.DataFrame()
    rules = evaluate_complex_genotypes(parsed.variants)
    cache_dir = storage.root / "cache" / "pgs"
    loaded = {}

    def scoring_loader(pgs_id: str) -> pd.DataFrame | None:
        if pgs_id not in loaded:
            loaded[pgs_id] = download_pgs_scoring_file(pgs_id, cache_dir)
        return loaded[pgs_id]

    scores = compute_pgs_scores(parsed.variants, scoring_loader=scoring_loader)
    reference_file = cache_dir / "eur_1000g_phase3_grch37.npz"
    reference_valid = True
    if reference_file.exists():
        try:
            validate_reference(reference_file)
        except (ValueError, KeyError, BadZipFile, EOFError):
            reference_valid = False
    if reference_valid:
        interpret_pgs(parsed.variants, scores, scoring_loader, _pgs_alleles_match, reference_file)
    else:
        for score in scores:
            score.update(eur_reason_code="invalid_reference", eur_reason="Файл EUR-референса повреждён.")
    resource_paths = [cache_dir / f"{pgs_id}_GRCh37.tsv" for pgs_id, frame in loaded.items() if frame is not None]
    if reference_file.exists():
        resource_paths.append(reference_file)
    report = build_report(patient_id, profile, parsed, clinvar, rules, scores, annotation_issue, resource_paths)
    storage.save_report(report)
    return report
