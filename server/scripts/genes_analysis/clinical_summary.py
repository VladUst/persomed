"""Краткая проверяемая сводка после полного генетического отчёта."""

from pathlib import Path

import pandas as pd
import yaml


RULES_FILE = Path(__file__).with_name("clinical_findings.yaml")


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


def _pgs_group(result: dict) -> str:
    trait = result.get("trait_en", "")
    if trait.startswith("Coronary"):
        return "Ишемическая болезнь сердца"
    return result["trait"].split(" (")[0]


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

    by_name = {item["gene"]: item for item in complex_results}
    h63d = by_name.get("HFE H63D")
    c282y = by_name.get("HFE C282Y")
    if h63d and c282y and h63d["status"] != "Не оценено" and c282y["status"] != "Не оценено":
        if h63d["risk_level"] == "Маркер" or c282y["risk_level"] in {"Носитель", "Высокий"}:
            role = (
                "Генотип, ассоциированный с перегрузкой железом — подтвердить"
                if c282y["risk_level"] == "Высокий" else
                "Маркер HFE; диагноз гемохроматоза не установлен"
            )
            findings.append({
                "gene": "HFE", "rsid": "rs1799945 / rs1800562",
                "genotype": f"H63D {h63d['genotype']}; C282Y {c282y['genotype']}",
                "condition": "Перегрузка железом", "role": role,
                "interpretation": "Генотип сопоставляется с показателями обмена железа и фенотипом.",
                "clinical_question": "Есть ли повышение насыщения трансферрина, ферритина или признаки перегрузки железом?",
                "next_step": "Если есть клиническое подозрение, оценить насыщение трансферрина и ферритин по профильным рекомендациям.",
                "limitation": "H63D сам по себе не подтверждает HFE-гемохроматоз.",
                "source": "https://easl.eu/wp-content/uploads/2022/06/PIIS01688278220021121.pdf",
            })
            summarized_variants.add("chr6:g.26091179C>G")

    hla = next((item for item in complex_results if item["gene"].startswith("HLA-B")), None)
    if hla and hla["risk_level"] == "Косвенный маркер":
        findings.append({
            "gene": "HLA-B", "rsid": "rs2395029", "genotype": hla["genotype"],
            "condition": "Гиперчувствительность к абакавиру",
            "role": "Косвенный лекарственный маркер — требуется типирование",
            "interpretation": "SNP связан с HLA-B*57:01, но не определяет HLA-аллель напрямую.",
            "clinical_question": "Планируется ли назначение абакавира?",
            "next_step": "Перед назначением получить прямой результат HLA-B*57:01-типирования.",
            "limitation": "По tag SNP нельзя назначать или отменять лекарство.",
            "source": "https://cpicpgx.org/wp-content/uploads/2016/01/CPIC_HLAB-Abacavir.pdf",
        })

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
    if not clinvar_df.empty:
        conflicting_ampd1 = clinvar_df[
            (clinvar_df["rsid"] == "rs17602729")
            & (clinvar_df["category"] == "Спорное заключение")
        ]
        if not conflicting_ampd1.empty:
            unevaluated.append("AMPD1 rs17602729: заключения ClinVar конфликтуют; диагноз по этому маркеру не установлен")

    candidate_variants = (
        set(clinvar_df.loc[clinvar_df["category"] == "Кандидат для проверки", "variant"])
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
            result.get("eur_quality") == "хорошая",
            result.get("coverage_pct", 0),
        )
        previous = pgs_by_group.get(group)
        if previous is None or priority > previous[0]:
            pgs_by_group[group] = (priority, result)

    return {
        "reviewed": rules["reviewed"],
        "findings": findings,
        "absent": absent,
        "unevaluated": unevaluated,
        "other_candidates": remaining_candidates,
        "pgs": [(group, value[1]) for group, value in pgs_by_group.items()],
    }


def print_clinical_summary(summary: dict) -> None:
    """Печатает краткий дополнительный этап после подробного отчёта."""
    print("\n" + "=" * 70)
    print(" ИТОГОВАЯ СВОДКА")
    print("=" * 70)
    print(f"  Правила сводки проверены: {summary['reviewed']}")
    print("  Это вопросы для врача; генотипы из VCF требуют подтверждения при")
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
        print(f"    Вопрос врачу: {item['clinical_question']}")
        print(f"    Проверить: {item['next_step']}")
        print(f"    Ограничение: {item['limitation']}")
        print(f"    Источник: {item['source']}")
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
