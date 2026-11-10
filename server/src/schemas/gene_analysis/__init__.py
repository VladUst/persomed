"""Публичный контракт отчёта: числа, причины пропусков и проверяемые ссылки."""

from datetime import date
from typing import Annotated, Generic, Literal, TypeVar
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

Percent = Annotated[float, Field(ge=0, le=100)]
SectionName = Literal["clinvar", "genotype_rules", "polygenic_scores"]


class Schema(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Issue(Schema):
    code: str
    message: str


class Profile(Schema):
    id: UUID
    filename: str
    size_bytes: int
    sha256: str
    uploaded_at: AwareDatetime
    sample_name: str
    genome_build: Literal["GRCh37"] = "GRCh37"
    build_source: Literal["declared", "assumed"]


class ProfileResponse(Schema):
    profile: Profile | None


class Source(Schema):
    url: str
    citation: str | None = None
    doi: str | None = None
    pubmed: str | None = None
    reference: str | None = None


class EvidenceRef(Schema):
    section: SectionName
    item_id: str


class Variant(Schema):
    genome_build: Literal["GRCh37"] = "GRCh37"
    chromosome: str
    position: int
    ref: str
    alt: str
    rsid: str | None


class Significance(Schema):
    original: str
    label: str


class ClinvarItem(Schema):
    id: str
    variant: Variant
    genes: list[str]
    genotype: str
    zygosity: str
    conditions: list[str]
    category: Literal["candidate", "conflicting", "uncertain", "association", "drug_response"]
    significance: Significance
    accession: str | None
    review_status: str | None
    last_evaluated: date | None
    source_url: str | None


class ObservedVariant(Schema):
    rsid: str
    genotype: str
    alleles: list[str]
    phased: bool
    phase_set: str | None


class RuleResult(Schema):
    code: str
    label: str
    explanation: str


class RuleEffect(Schema):
    type: Literal["OR"] = "OR"
    value: float
    context: str
    sources: list[Source]


class GenotypeRuleItem(Schema):
    id: str
    genes: list[str]
    condition: str
    status: Literal["evaluated", "not_evaluated"]
    reason: Issue | None
    observed_variants: list[ObservedVariant]
    diplotype: str | None
    result: RuleResult | None
    effect: RuleEffect | None
    limitations: list[str]
    sources: list[Source]


class Interval(Schema):
    lower: float
    upper: float

    @model_validator(mode="after")
    def ordered(self):
        if self.lower > self.upper:
            raise ValueError("Границы интервала должны быть упорядочены")
        return self


class Coverage(Schema):
    total: int
    matched: int
    imputed: int
    skipped: int
    measured_percent: Percent
    effective_percent: Percent


class ReferenceComparison(Schema):
    status: Literal["evaluated", "not_evaluated"]
    reason: Issue | None
    population: Literal["EUR"] = "EUR"
    sample_count: int | None
    reference_snps: int | None
    patient_snps: int | None
    percentile: Percent | None
    category: str | None
    category_label: str | None
    z_score: float | None


class Stability(Schema):
    quality: Literal["good", "limited", "low"]
    r_squared: Annotated[float, Field(ge=0, le=1)]
    tier_agreement: Annotated[float, Field(ge=0, le=1)]
    percentile_interval: Interval


class ResearchEffect(Schema):
    type: Literal["HR"] = "HR"
    value: float
    range: Interval
    outcome: str
    source_url: str
    note: str


class PolygenicScoreItem(Schema):
    pgs_id: str
    trait_id: str
    trait: str
    source_url: str
    status: Literal["evaluated", "not_evaluated"]
    reason: Issue | None
    coverage: Coverage | None
    raw_score: float | None
    reference_comparison: ReferenceComparison
    stability: Stability | None
    research_effect: ResearchEffect | None


Item = TypeVar("Item")


class Section(Schema, Generic[Item]):
    status: Literal["complete", "partial", "unavailable"]
    issues: list[Issue] = Field(default_factory=list)
    items: list[Item] = Field(default_factory=list)


class Finding(Schema):
    id: str
    genes: list[str]
    condition: str
    role: str
    interpretation: str
    clinical_question: str
    next_step: str
    limitations: list[str]
    evidence_refs: list[EvidenceRef]
    sources: list[Source]


class SummaryNotice(Schema):
    message: str
    evidence_refs: list[EvidenceRef]


class PolygenicOverview(Schema):
    trait_id: str
    trait: str
    pgs_id: str


class Summary(Schema):
    findings: list[Finding]
    not_detected: list[SummaryNotice]
    not_evaluated: list[SummaryNotice]
    polygenic_overview: list[PolygenicOverview]
    other_candidate_variants_count: int | None


class Quality(Schema):
    total_records: int
    usable_records: int
    skipped_records: int
    alt_records: int
    unmatched_annotations: int
    issues: list[Issue]


class ResourceVersion(Schema):
    name: str
    sha256: str


class Provenance(Schema):
    rules_reviewed: date
    resources: list[ResourceVersion]
    sources: list[Source]
    annotation_cache_policy: str


class GeneAnalysisReport(Schema):
    schema_version: Literal["1.0"] = "1.0"
    analysis_version: str
    patient_id: int
    profile: Profile
    generated_at: AwareDatetime
    status: Literal["complete", "partial"]
    summary: Summary
    clinvar: Section[ClinvarItem]
    genotype_rules: Section[GenotypeRuleItem]
    polygenic_scores: Section[PolygenicScoreItem]
    quality: Quality
    limitations: list[str]
    provenance: Provenance

    @model_validator(mode="after")
    def check_references(self):
        """Каждая ссылка сводки должна вести к существующей строке таблицы."""
        ids = {
            "clinvar": {item.id for item in self.clinvar.items},
            "genotype_rules": {item.id for item in self.genotype_rules.items},
            "polygenic_scores": {item.pgs_id for item in self.polygenic_scores.items},
        }
        for entry in [*self.summary.findings, *self.summary.not_detected, *self.summary.not_evaluated]:
            for ref in entry.evidence_refs:
                if ref.item_id not in ids[ref.section]:
                    raise ValueError("Ссылка сводки не соответствует результатам анализа")
        for entry in self.summary.polygenic_overview:
            if entry.pgs_id not in ids["polygenic_scores"]:
                raise ValueError("Модель сводки отсутствует в подробном отчёте")
        return self
