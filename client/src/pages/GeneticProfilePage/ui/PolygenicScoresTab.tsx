import type { GeneReport } from "../api/genes";
import type { PolygenicScoreItem, ReportDetail } from "../model/report";
import { formatNumber, resultStatus } from "./reportFormatting";
import { ResultsTable, type TableRowData } from "./ResultsTable";
import { SectionHeading } from "./SectionHeading";

const pgsColumnHints: Record<string, string> = {
  Заболевание:
    "Заболевание или показатель, для которого создана модель. Число SNP в скобках показывает, сколько генетических позиций входит в модель, а не сколько изменений найдено у пациента. Для одного признака в отчёте может быть несколько моделей.",
  Модель:
    "Номер модели в PGS Catalog. Разные модели одного признака используют разные наборы SNP и разные веса для расчёта балла. Откройте строку таблицы, чтобы перейти к источнику именно этой модели.",
  Статус:
    "«Оценено» означает, что балл по этой модели удалось рассчитать. При этом часть SNP могла отсутствовать в VCF, поэтому рядом нужно проверить измеренное покрытие. «Не оценено» означает, что расчёт не выполнен, например из-за недостатка найденных SNP или неподходящего файла весов.",
  "EUR-перцентиль":
    "Положение рассчитанного балла среди баллов EUR-образцов в референсной выборке. Например, 80-й перцентиль означает, что балл пациента выше примерно 80% баллов в этой выборке. Это не означает 80% вероятности заболевания. «Не рассчитан» означает, что сравнение с выборкой выполнить не удалось; причина есть в подробностях модели.",
  "Измеренное покрытие":
    "Доля SNP модели, для которых в VCF найден генотип пациента и подтверждено совпадение координаты и аллелей. Например, 40% означает, что напрямую учтены 40 из 100 SNP модели. SNP, для которых вместо генотипа подставлено среднее значение по популяции, в этот процент не входят.",
};

const getPgsRows = (items: PolygenicScoreItem[]): TableRowData[] =>
  items.map((item) => ({
    id: item.pgs_id,
    cells: [
      item.trait,
      item.pgs_id,
      resultStatus(item.status),
      item.reference_comparison.percentile == null
        ? "Не рассчитан"
        : formatNumber(item.reference_comparison.percentile),
      item.coverage ? `${formatNumber(item.coverage.measured_percent)}%` : "—",
    ],
    search: [
      item.trait,
      item.pgs_id,
      item.reference_comparison.category_label,
      item.reason?.message,
    ].join(" "),
    detail: { kind: "pgs", item },
  }));

export const PolygenicScoresTab = ({
  report,
  onOpen,
}: {
  report: GeneReport;
  onOpen: (detail: ReportDetail) => void;
}) => (
  <>
    <SectionHeading title="Полигенные оценки по моделям PGS Catalog" />
    <ResultsTable
      headers={[
        "Заболевание",
        "Модель",
        "Статус",
        "EUR-перцентиль",
        "Измеренное покрытие",
      ]}
      headerHints={pgsColumnHints}
      rows={getPgsRows(report.polygenic_scores.items ?? [])}
      onOpen={onOpen}
      emptyLabel="Полигенные модели отсутствуют в отчёте."
    />
  </>
);
