import type { GeneReport } from "../api/genes";
import type { GenotypeRuleItem, ReportDetail } from "../model/report";
import { resultStatus } from "./reportFormatting";
import { ResultsTable, type TableRowData } from "./ResultsTable";
import { SectionHeading } from "./SectionHeading";

const getRuleRows = (items: GenotypeRuleItem[]): TableRowData[] =>
  items.map((item) => ({
    id: item.id,
    cells: [
      item.condition,
      item.genes.join(", "),
      resultStatus(item.status),
      item.result?.label ?? item.reason?.message ?? "—",
      item.diplotype ?? "—",
    ],
    search: [
      item.condition,
      item.genes,
      item.id,
      item.result?.label,
      item.reason?.message,
    ].join(" "),
    detail: { kind: "rule", item },
  }));

export const GenotypeRulesTab = ({
  report,
  onOpen,
}: {
  report: GeneReport;
  onOpen: (detail: ReportDetail) => void;
}) => (
  <>
    <SectionHeading title="Правила генотипов" />
    <ResultsTable
      headers={[
        "Состояние",
        "Гены",
        "Оценка",
        "Результат или причина",
        "Диплотип",
      ]}
      rows={getRuleRows(report.genotype_rules.items ?? [])}
      onOpen={onOpen}
      emptyLabel="Правила отсутствуют в отчёте."
    />
  </>
);
