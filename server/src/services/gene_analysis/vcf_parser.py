"""Чтение одного диплоидного образца с сохранением референсных вызовов."""

import re
from pathlib import Path

import pandas as pd
import vcf

from .errors import GeneAnalysisError
from .types import ParsedProfile


def parse_vcf(path: Path) -> ParsedProfile:
    """Проверяет VCF и собирает пригодные вызовы; пропуск не равен 0/0."""
    records = []
    total = 0
    try:
        with path.open(encoding="utf-8-sig") as source:
            if not source.readline().startswith("##fileformat=VCFv4."):
                raise GeneAnalysisError("Файл должен содержать заголовок VCF версии 4.")
            source.seek(0)
            reader = vcf.Reader(source)
            if len(reader.samples) != 1:
                raise GeneAnalysisError("VCF должен содержать ровно один образец.")
            references = [str(reader.metadata.get("reference", "")), str(reader.metadata.get("assembly", ""))]
            # assembly также может находиться в метаданных contig.
            source.seek(0)
            for line in source:
                if not line.startswith("#"):
                    break
                if line.startswith("##contig="):
                    references.extend(re.findall(r'assembly=([^,>]+)', line))
            build = " ".join(references).lower()
            if re.search(r"grch(?!37\b)\d+|hg(?!19\b)\d+|hs1|chm13", build):
                raise GeneAnalysisError("Поддерживается только сборка GRCh37/hg19.")
            build_source = "declared" if re.search(r"grch37|hg19|human_g1k_v37", build) else "assumed"
            source.seek(0)
            reader = vcf.Reader(source)
            for record in reader:
                total += 1
                sample = record.samples[0]
                indices = sample.gt_alleles
                if indices is None or len(indices) != 2 or any(
                    index is None or not str(index).isdigit() for index in indices
                ):
                    continue
                alleles = [record.REF] + [str(alt) for alt in record.ALT]
                first, second = map(int, indices)
                if max(first, second) >= len(alleles):
                    continue
                records.append({
                    "chrom": record.CHROM, "pos": record.POS, "rsid": record.ID,
                    "ref": record.REF, "alt": ",".join(str(alt) for alt in record.ALT),
                    "genotype": sample["GT"], "allele_1": alleles[first], "allele_2": alleles[second],
                    "zygosity": {0: "homozygous_ref", 1: "heterozygous", 2: "homozygous_alt"}.get(sample.gt_type, "unknown"),
                    "phased": sample.phased,
                    "phase_set": sample["PS"] if "PS" in sample.data._fields else None,
                })
            sample_name = reader.samples[0]
    except (ValueError, IndexError, AttributeError, KeyError, TypeError, StopIteration, UnicodeError) as exc:
        raise GeneAnalysisError("Не удалось прочитать структуру записей VCF.") from exc
    if not records:
        raise GeneAnalysisError("В VCF нет пригодных диплоидных генотипов.")
    return ParsedProfile(pd.DataFrame(records), sample_name, build_source, total, total - len(records))
