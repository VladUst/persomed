import pandas as pd


CLINVAR_CATEGORIES = {
    "pathogenic": "candidate",
    "likely pathogenic": "candidate",
    "pathogenic/likely pathogenic": "candidate",
    "conflicting interpretations of pathogenicity": "conflicting",
    "uncertain significance": "uncertain",
    "risk factor": "association",
    "association": "association",
    "affects": "association",
    "drug response": "drug_response",
}


def _matching_snv(annotation: dict, variant: dict) -> bool:
    """Проверяет hg19 SNV, включая альтернативный аллель в генотипе."""
    clinvar = annotation.get("clinvar")
    if not isinstance(clinvar, dict):
        return False
    chrom = str(variant["chrom"]).removeprefix("chr")
    ref, alt = str(variant["ref"]).upper(), str(variant["alt"]).upper()
    if len(ref) != 1 or len(alt) != 1 or ref not in "ACGT" or alt not in "ACGT":
        return False
    if alt not in {variant["allele_1"], variant["allele_2"]}:
        return False
    position = int(variant["pos"])
    hg19 = clinvar.get("hg19")
    return (
        annotation.get("_id") == f"chr{chrom}:g.{position}{ref}>{alt}"
        and str(clinvar.get("chrom")) == chrom
        and clinvar.get("ref") == ref
        and clinvar.get("alt") == alt
        and isinstance(hg19, dict)
        and hg19.get("start") == position
        and hg19.get("end") == position
    )


def extract_clinvar_significance(annotations: list[dict], variants_df: pd.DataFrame) -> pd.DataFrame:
    """Возвращает ClinVar-записи только для точно сопоставленных hg19 SNP."""
    clinvar_records = []
    annotated_ids = {
        ann.get("query") for ann in annotations
        if isinstance(ann.get("clinvar"), dict)
    }
    variants_by_rsid = {}
    for variant in variants_df[variants_df["rsid"].isin(annotated_ids)].to_dict("records"):
        variants_by_rsid.setdefault(variant["rsid"], []).append(variant)
    unmatched = 0

    for ann in annotations:
        if ann.get("notfound"):
            continue

        query_rsid = ann.get("query", "")
        clinvar = ann.get("clinvar")
        if not isinstance(clinvar, dict):
            continue
        matching = [
            variant for variant in variants_by_rsid.get(query_rsid, [])
            if _matching_snv(ann, variant)
        ]
        if len(matching) != 1:
            unmatched += 1
            continue
        variant = matching[0]

        # ClinVar может вернуть один объект или список
        rcv_list = clinvar.get("rcv", [])
        if isinstance(rcv_list, dict):
            rcv_list = [rcv_list]

        for rcv in rcv_list:
            significance = rcv.get("clinical_significance", "")
            if not isinstance(significance, str):
                continue
            category = CLINVAR_CATEGORIES.get(significance.strip().casefold())
            if category is None:
                continue
            conditions = rcv.get("conditions", {})
            condition_name = ""

            if isinstance(conditions, dict):
                condition_name = conditions.get("name", "")
            elif isinstance(conditions, list):
                condition_name = "; ".join(
                    c.get("name", "") for c in conditions if isinstance(c, dict)
                )

            gene_info = clinvar.get("gene", {})
            gene_name = ""
            if isinstance(gene_info, dict):
                gene_name = gene_info.get("symbol", "")
            elif isinstance(gene_info, list):
                gene_name = ", ".join(
                    g.get("symbol", "") for g in gene_info if isinstance(g, dict)
                )

            clinvar_records.append({
                "rsid": query_rsid,
                "variant": ann["_id"],
                "clinvar_id": rcv.get("accession", ""),
                "gene": gene_name,
                "significance": significance,
                "category": category,
                "condition": condition_name,
                "genotype": f"{variant['allele_1']}/{variant['allele_2']}",
                "zygosity": variant["zygosity"],
                "review_status": rcv.get("review_status", ""),
                "last_evaluated": rcv.get("last_evaluated", ""),
            })

    df = pd.DataFrame(clinvar_records)
    if not df.empty:
        df = df.drop_duplicates(subset=["variant", "clinvar_id", "significance", "condition"])
    df.attrs["unmatched_annotations"] = unmatched
    return df
