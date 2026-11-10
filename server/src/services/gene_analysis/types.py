"""Внутренний результат чтения VCF, не передаваемый напрямую в API."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class ParsedProfile:
    variants: pd.DataFrame
    sample_name: str
    build_source: str
    total_records: int
    skipped_records: int
