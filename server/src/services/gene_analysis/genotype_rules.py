"""Декларативные SNP- и гаплотипные правила без вывода в консоль."""

import pandas as pd
import yaml

from .config import RESOURCES


def load_rules() -> list[dict]:
    with (RESOURCES / "complex_genotypes.yaml").open(encoding="utf-8") as source:
        return yaml.safe_load(source)["rules"]


def _haplotype(rule: dict, alleles: dict[str, str]) -> str:
    for haplotype in rule["haplotype_rules"]:
        if all(alleles.get(rsid) == allele for rsid, allele in haplotype["alleles"].items()):
            return haplotype["name"]
    return "?"


def evaluate_complex_genotypes(variants_df: pd.DataFrame) -> list[dict]:
    """Не подменяет отсутствующий или неоднозначный локус референсным генотипом."""
    lookup = {}
    for row in variants_df.to_dict("records"):
        lookup.setdefault(row["rsid"], []).append(row)
    results = []
    for rule in load_rules():
        required = rule.get("required_snps", [rule.get("snp")])
        choices = rule["diplotype_risk"] if rule["type"] == "haplotype" else rule["genotypes"]
        result = {
            "id": rule["id"], "gene": rule["name"], "genotype": "—",
            "rsids": required,
            "disease": next(iter(choices.values()))["disease"], "status": "not_evaluated",
            "risk_level": "Не оценено", "risk_code": None, "details": "", "reason_code": None,
            "effect": None, "sources": rule["sources"], "observed": [],
        }
        rows = [row for rsid in required for row in lookup.get(rsid, [])]
        result["observed"] = rows
        ambiguous = [rsid for rsid in required if len(lookup.get(rsid, [])) > 1]
        missing = [rsid for rsid in required if not lookup.get(rsid)]
        if ambiguous:
            result.update(reason_code="ambiguous_variant", details=f"Неоднозначные записи: {', '.join(ambiguous)}")
        elif missing:
            result.update(reason_code="missing_variant", details=f"Отсутствует: {', '.join(missing)}")
        elif rule["type"] == "haplotype":
            heterozygous = [row for row in rows if row["allele_1"] != row["allele_2"]]
            phase_sets = {row["phase_set"] for row in heterozygous}
            # При двух гетерозиготах одинаковый PS нужен для совместной фазы.
            if len(heterozygous) > 1 and (
                not all(row["phased"] for row in heterozygous)
                or any(pd.isna(value) for value in phase_sets) or len(phase_sets) != 1
            ):
                result.update(reason_code="unknown_phase", details="Фаза между вариантами не подтверждена")
            else:
                haplotypes = [_haplotype(rule, {row["rsid"]: row[key] for row in rows})
                              for key in ("allele_1", "allele_2")]
                diplotype = "/".join(sorted(haplotypes))
                result["genotype"] = diplotype
                _apply_choice(result, choices.get(diplotype))
        else:
            row = rows[0]
            result["genotype"] = f"{row['allele_1']}/{row['allele_2']}"
            allele = rule["risk_allele"]
            if allele not in {row["ref"], row["alt"]}:
                result.update(reason_code="allele_mismatch", details=f"Аллель {allele} отсутствует среди REF/ALT")
            else:
                copies = int(row["allele_1"] == allele) + int(row["allele_2"] == allele)
                _apply_choice(result, choices[{0: "0/0", 1: "0/1", 2: "1/1"}[copies]])
        results.append(result)
    return results


def _apply_choice(result: dict, choice: dict | None) -> None:
    """Сохраняет машинный код отдельно от формулировки исходного правила."""
    if choice is None:
        result.update(reason_code="unsupported_diplotype", details="Для этого диплотипа нет правила интерпретации")
        return
    result.update(status="evaluated", risk_level=choice["level"], risk_code=choice["code"],
                  details=choice.get("details", ""), effect=choice.get("or"))
