"""Консольная сводка использует те же правила находок, что и API."""

import sys
from pathlib import Path

import pandas as pd

SERVER_ROOT = Path(__file__).resolve().parents[2]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from src.services.gene_analysis.clinical_summary import build_clinical_summary as build_report_summary
from src.services.gene_analysis.genotype_rules import evaluate_complex_genotypes


def build_clinical_summary(
    variants_df: pd.DataFrame,
    clinvar_df: pd.DataFrame,
    complex_results: list[dict],
    pgs_results: list[dict],
) -> dict:
    """Приводит консольные результаты к формату общего движка находок."""
    normalized_clinvar = clinvar_df.copy()
    if not normalized_clinvar.empty:
        normalized_clinvar["category"] = normalized_clinvar["category"].replace(
            {"Кандидат для проверки": "candidate"}
        )
    normalized_pgs = [
        {**item, "eur_quality": "good" if item.get("eur_quality") == "хорошая"
         else item.get("eur_quality")}
        for item in pgs_results
    ]
    summary = build_report_summary(
        variants_df, normalized_clinvar,
        evaluate_complex_genotypes(variants_df), normalized_pgs,
    )

    by_name = {item["gene"]: item for item in complex_results}
    absent = []
    for gene, label in [
        ("F5 (Factor V Leiden)", "F5 Leiden"),
        ("F2 (Prothrombin G20210A)", "F2 G20210A"),
        ("HFE C282Y", "HFE C282Y"),
    ]:
        item = by_name.get(gene)
        if item and item["status"] != "Не оценено" and item["risk_level"] == "Аллель не выявлен":
            absent.append(f"{label}: указанный аллель не выявлен ({item['genotype']})")

    unevaluated = [
        f"{item['gene']}: {item['details']}"
        for item in complex_results if item["status"] == "Не оценено"
    ]
    return {**summary, "absent": absent, "unevaluated": unevaluated}


def print_clinical_summary(summary: dict) -> None:
    """Печатает краткий дополнительный этап после подробного отчёта."""
    print("\n" + "=" * 70)
    print(" ИТОГОВАЯ СВОДКА")
    print("=" * 70)
    print(f"  Правила сводки проверены: {summary['reviewed']}")
    print("  Это поводы для проверки; генотипы из VCF требуют подтверждения при")
    print("  принятии медицинских решений.")
    print("  Для PGS предполагается сходство пациента с EUR-выборкой; происхождение")
    print("  не проверяется этим скриптом.")

    print("\n  ОБНАРУЖЕННЫЕ МАРКЕРЫ И КАНДИДАТЫ ДЛЯ ПРОВЕРКИ")
    if not summary["findings"]:
        print("  Среди отобранных вариантов точных находок нет.")
    for item in summary["findings"]:
        print(f"\n  {item['gene']} {item['rsid']} ({item['genotype']}) — {item['role']}")
        print(f"    Связанный признак: {item['condition']}")
        print(f"    Основание: {item['interpretation']}")
        if item.get("clinvar_review_status"):
            print(f"    ClinVar: {item['clinvar_id']}; review status: "
                  f"{item['clinvar_review_status']}; оценено: "
                  f"{item.get('clinvar_last_evaluated') or 'дата неизвестна'}")
        print(f"    Рекомендация: {item['recommendation']}")
        for source in item["sources"]:
            print(f"    Источник: {source}")
    print(f"\n  Других уникальных вариантов с P/LP-записями ClinVar: "
          f"{summary['other_candidates']}; они есть в подробном разделе и не")
    print("  получили автоматической клинической оценки без проверки доказательств.")

    print("\n  ПРОВЕРЕННЫЕ АЛЛЕЛИ, КОТОРЫЕ НЕ ВЫЯВЛЕНЫ")
    for line in summary["absent"]:
        print(f"  • {line}")
    if not summary["absent"]:
        print("  Нет таких результатов среди отобранных правил.")
    print("  Отсутствие этих аллелей не означает низкий общий риск заболевания.")

    print("\n  НЕОПРЕДЕЛЁННЫЕ И НЕПОЛНЫЕ ДАННЫЕ")
    for line in summary["unevaluated"]:
        print(f"  • {line}")
    if not summary["unevaluated"]:
        print("  Среди отобранных правил нет пропусков.")

    print("\n  ПОЛИГЕННЫЕ МОДЕЛИ: ОТНОСИТЕЛЬНАЯ ГЕНЕТИЧЕСКАЯ ПРЕДРАСПОЛОЖЕННОСТЬ")
    for group, result in summary["pgs"]:
        measured = (
            f"{result['matched']}/{result['total']} ({result['coverage_pct']}%)"
            if "matched" in result else "нет данных"
        )
        print(f"\n  • {group} — {result['pgs_id']}")
        if "eur_percentile" in result:
            print(f"    Генетическая предрасположенность: {result['eur_tier']}; "
                  f"{result['eur_percentile']}-й перцентиль EUR-референса.")
            low_pct, high_pct = result["eur_percentile_interval"]
            print(f"    Ориентировочный диапазон полного балла из-за пропущенных SNP: "
                  f"{low_pct}–{high_pct}-й перцентили (5–95% остатков EUR-референса).")
            print(f"    Устойчивость категории пациента по этому диапазону: "
                  f"{result['eur_quality']}.")
            print(f"    В EUR-выборке: R² полного и частичного балла "
                  f"{result['eur_r2']:.2f}; совпадение категорий "
                  f"{result['eur_tier_agreement']:.0%}.")
            if "eur_relative_hr" in result:
                low, high = result["eur_relative_hr_range"]
                print(f"    Ориентир для исхода «{result['eur_outcome']}»: "
                      f"относительная интенсивность события ×{result['eur_relative_hr']:.2f} "
                      f"(интервал по опубликованному HR ×{low:.2f}–×{high:.2f}).")
                print(f"    {result['eur_hr_note']}")
            else:
                print("    Численный риск заболевания для этой версии модели не валидирован.")
            if result["pgs_id"] == "PGS000025":
                print("    Эта модель не включает APOE; общий риск болезни Альцгеймера по ней не установлен.")
        else:
            print(f"    Категория не определена: {result.get('eur_reason', result['status'])}.")
        reference_overlap = (
            f"; для EUR-сравнения: {result['eur_matched_snps']}/"
            f"{result['eur_reference_snps']} SNP референса"
            if "eur_matched_snps" in result else ""
        )
        print(f"    Измерено SNP пациента: {measured}{reference_overlap}; "
              f"EUR-образцов: {result.get('eur_samples', '—')}.")
        if result.get("source"):
            print(f"    Модель: {result['source']}")
    print("\n  Категория описывает положение PGS среди 503 EUR-образцов 1000 Genomes,")
    print("  а не вероятность диагноза. Пороги 20/40/60/80/95 — условная шкала отчёта.")
    print("  Абсолютный риск за 10 лет из одного VCF не рассчитывается: нужны")
    print("  возраст, пол, клинические данные и модель того же исхода.")
