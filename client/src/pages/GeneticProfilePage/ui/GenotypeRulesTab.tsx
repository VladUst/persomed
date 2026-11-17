import Stack from "@mui/material/Stack";
import type { GeneReport } from "../api/genes";
import type { Finding, GenotypeRuleItem, ReportDetail } from "../model/report";
import { resultStatus } from "./reportFormatting";
import { ResultsTable, type TableRowData } from "./ResultsTable";
import { SectionHeading } from "./SectionHeading";

const getFindingRows = (items: Finding[]): TableRowData[] =>
  items.map((item) => ({
    id: item.id,
    cells: [
      item.condition,
      item.genes.join(", "),
      item.role,
      item.interpretation,
      item.recommendation,
    ],
    search: [
      item.condition,
      item.genes,
      item.role,
      item.interpretation,
      item.recommendation,
    ].join(" "),
    detail: { kind: "finding", item },
  }));

const getRuleRows = (items: GenotypeRuleItem[]): TableRowData[] =>
  items.map((item) => ({
    id: item.id,
    cells: [
      item.genes.join(", "),
      item.condition,
      item.rsids.join(", "),
      resultStatus(item.status),
      item.result?.label ?? item.reason?.message ?? "—",
    ],
    search: [
      item.condition,
      item.genes,
      item.rsids,
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
  <Stack spacing={3}>
    <div>
      <SectionHeading title="Оценки по правилам" />
      <ResultsTable
        headers={[
          "Заболевание или признак",
          "Ген",
          "Заключение",
          "Интерпретация",
          "Рекомендация",
        ]}
        rows={getFindingRows(report.summary.findings)}
        onOpen={onOpen}
        emptyLabel="Находок по правилам нет."
        tableLabel="Оценки по правилам"
        tableMinWidth={1200}
      />
    </div>
    <div>
      <SectionHeading title="Комплексные генотипы" />
      <ResultsTable
        headers={[
          "Ген",
          "Заболевание или признак",
          "Варианты",
          "Статус",
          "Результат",
        ]}
        rows={getRuleRows(report.genotype_rules.items ?? [])}
        onOpen={onOpen}
        emptyLabel="Комплексные генотипы отсутствуют в отчёте."
        tableLabel="Комплексные генотипы"
      />
    </div>
  </Stack>
);
