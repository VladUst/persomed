"""
Проверка кандидатов PGS Catalog на пригодность для платформы.

Что проверяется для каждого PGS ID:
  - Скачивается ли scoring-файл (harmonized GRCh37)
  - Есть ли колонка `allelefrequency_effect` (EAF) — критично для z-score
  - Сколько строк EAF реально заполнено (бывает: колонка есть, но пустая)
  - Общее число вариантов

Использование:
    python check_pgs_candidates.py

После прогона:
  - Выбери из вывода скоры с "EAF ✓" и большим % заполненных EAF
  - Замени соответствующие записи в DEFAULT_PGS_SCORES в analysis.py
  - Скоры без EAF можно оставить — они тоже считают score, но без
    перцентиля; либо удалить, чтобы не загромождать отчёт.

Файлы кэшируются в .pgs_cache/, повторный запуск работает оффлайн.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from analysis import download_pgs_scoring_file  # noqa: E402

# Кандидаты для проверки.
# Степень уверенности у разных ID РАЗНАЯ — поэтому и нужен этот скрипт:
# одни 100% существуют (уже в коде), другие — образованные догадки на
# основе литературы. Скрипт покажет правду.
CANDIDATES = {
    "Болезнь Альцгеймера": [
        "PGS000025",   # уже в коде
        "PGS000026",   # уже в коде (без EAF — проверим)
        # Кандидаты на замену / добавление:
        "PGS000334",
        "PGS000776",
        "PGS000777",
        "PGS000778",
        "PGS001775",
        "PGS002280",
        "PGS003957",
    ],
    "ИБС / Коронарная болезнь сердца": [
        "PGS000010",   # уже в коде
        "PGS000011",   # уже в коде
        "PGS000019",   # уже в коде
        # Кандидаты:
        "PGS000013",
        "PGS000018",   # Khera 2018, известный, но 6.6M вариантов — может быть тяжёлым
        "PGS000058",
        "PGS000059",
        "PGS000337",
        "PGS000841",
        "PGS002048",
    ],
    "Сахарный диабет 2 типа": [
        # Первый раунд (проверено: все без EAF):
        # "PGS000031", "PGS000014", "PGS000036", "PGS000330",
        # "PGS000729", "PGS000805", "PGS001357", "PGS002308",
        #
        # Второй раунд — пробуем диапазоны рядом с теми ID, что для
        # Альцгеймера и ИБС оказались с EAF (PGS000010-59, PGS001775, PGS002280):
        "PGS000037",
        "PGS000038",
        "PGS000039",
        "PGS000040",
        "PGS000041",
        "PGS000042",
        "PGS000043",
        "PGS000063",
        "PGS000064",
        "PGS000065",
        "PGS000066",
        "PGS000067",
        "PGS001768",
        "PGS001769",
        "PGS001770",
        "PGS001771",
        "PGS001772",
        "PGS001773",
        "PGS001774",
        "PGS002243",
        "PGS002244",
        "PGS002245",
        "PGS002246",
        "PGS002247",
        "PGS002281",
        "PGS002282",
        "PGS002283",
    ],
}


def check_pgs(pgs_id: str) -> dict:
    """Загружает scoring-файл и собирает диагностику."""
    try:
        df = download_pgs_scoring_file(pgs_id)
    except Exception as e:
        return {"status": f"ошибка: {type(e).__name__}", "n": 0, "has_eaf": False}

    if df is None:
        return {"status": "недоступен", "n": 0, "has_eaf": False}

    has_eaf = "allelefrequency_effect" in df.columns
    eaf_filled = 0
    eaf_pct = 0.0
    if has_eaf:
        eaf_filled = int(df["allelefrequency_effect"].notna().sum())
        eaf_pct = round(eaf_filled / len(df) * 100, 1) if len(df) > 0 else 0.0

    # Проверяем и наличие rsID-колонки
    rsid_col = None
    for col in ("hm_rsID", "rsID"):
        if col in df.columns:
            rsid_col = col
            break

    return {
        "status": "OK",
        "n": len(df),
        "has_eaf": has_eaf,
        "eaf_filled": eaf_filled,
        "eaf_pct": eaf_pct,
        "rsid_col": rsid_col,
    }


def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print("=" * 78)
    print("  Проверка кандидатов PGS Catalog (harmonized GRCh37)")
    print("=" * 78)
    print()
    print("  Колонки:")
    print("    n       — число вариантов в scoring-файле")
    print("    EAF     — есть ли колонка allelefrequency_effect")
    print("    EAF%    — какой % строк EAF реально заполнен")
    print("    rsID    — название колонки с rsID (hm_rsID — harmonized)")
    print()

    verdict = {}  # pgs_id -> "годен" / "без EAF" / "недоступен"

    for trait, ids in CANDIDATES.items():
        print(f"\n--- {trait} ---")
        print(f"  {'PGS ID':<12} {'n':>7}  {'EAF':<4} {'EAF%':>6}  {'rsID':<10} {'статус'}")
        print(f"  {'-'*12} {'-'*7}  {'-'*4} {'-'*6}  {'-'*10} {'-'*20}")

        for pgs_id in ids:
            info = check_pgs(pgs_id)

            if info["status"] != "OK":
                print(f"  {pgs_id:<12} {'—':>7}  {'—':<4} {'—':>6}  {'—':<10} {info['status']}")
                verdict[pgs_id] = "недоступен"
                continue

            eaf_mark = "✓" if info["has_eaf"] else "✗"
            eaf_pct_str = f"{info['eaf_pct']}%" if info["has_eaf"] else "—"
            rsid_col_str = info["rsid_col"] or "нет!"

            if info["has_eaf"] and info["eaf_pct"] >= 90:
                status = "ГОДЕН — заполненный EAF"
                verdict[pgs_id] = "годен"
            elif info["has_eaf"] and info["eaf_pct"] >= 50:
                status = "частично — EAF неполный"
                verdict[pgs_id] = "частично"
            elif info["has_eaf"]:
                status = "EAF почти пустой"
                verdict[pgs_id] = "плохо"
            else:
                status = "БЕЗ EAF — нет перцентиля"
                verdict[pgs_id] = "без EAF"

            print(
                f"  {pgs_id:<12} {info['n']:>7}  {eaf_mark:<4} "
                f"{eaf_pct_str:>6}  {rsid_col_str:<10} {status}"
            )

    # Итоговая сводка
    print("\n" + "=" * 78)
    print("  ИТОГОВАЯ СВОДКА")
    print("=" * 78)

    by_verdict = {"годен": [], "частично": [], "плохо": [], "без EAF": [], "недоступен": []}
    for pgs_id, v in verdict.items():
        by_verdict[v].append(pgs_id)

    print(f"\n  ✓ ГОДНЫ к использованию (EAF >= 90%): {len(by_verdict['годен'])}")
    if by_verdict["годен"]:
        print(f"      {', '.join(by_verdict['годен'])}")

    print(f"\n  ~ Частично годны (EAF 50-90%):         {len(by_verdict['частично'])}")
    if by_verdict["частично"]:
        print(f"      {', '.join(by_verdict['частично'])}")

    print(f"\n  ✗ Без EAF (score можно, перцентиля нет): {len(by_verdict['без EAF'])}")
    if by_verdict["без EAF"]:
        print(f"      {', '.join(by_verdict['без EAF'])}")

    print(f"\n  ✗ Недоступны (404 или ошибка):           {len(by_verdict['недоступен'])}")
    if by_verdict["недоступен"]:
        print(f"      {', '.join(by_verdict['недоступен'])}")

    print()
    print("  Следующий шаг: в analysis.py обнови DEFAULT_PGS_SCORES,")
    print("  оставив только ID из категорий ✓ ГОДНЫ (и при желании ~ частично).")
    print("=" * 78)


if __name__ == "__main__":
    main()
