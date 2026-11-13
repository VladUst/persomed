import { useState } from "react";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import type { GeneReport } from "../api/genes";
import type { ClinvarItem, ReportDetail } from "../model/report";
import { clinvarReviewStatus, clinvarSignificance } from "./clinvarFormatting";
import { ResultsTable, type TableRowData } from "./ResultsTable";
import { SectionHeading } from "./SectionHeading";

const clinvarCategories: Array<{
  key: ClinvarItem["category"];
  title: string;
}> = [
  { key: "candidate", title: "Патогенные и вероятно патогенные" },
  { key: "association", title: "Ассоциации с заболеваниями и признаками" },
  {
    key: "drug_response",
    title: "Варианты, связанные с реакциями на лекарства",
  },
  { key: "conflicting", title: "Противоречивые классификации" },
  { key: "uncertain", title: "Варианты неопределённой клинической значимости" },
];

const getClinvarRows = (items: ClinvarItem[]): TableRowData[] =>
  items.map((item) => ({
    id: item.id,
    cells: [
      item.genes.join(", ") || "Вариант",
      item.genotype,
      item.conditions.join("; "),
      clinvarSignificance(item.significance.original),
      clinvarReviewStatus(item.review_status),
    ],
    search: [
      item.genes,
      item.conditions,
      item.variant.rsid,
      item.accession,
      item.significance.original,
      clinvarSignificance(item.significance.original),
      clinvarReviewStatus(item.review_status),
    ].join(" "),
    detail: { kind: "clinvar", item },
  }));

export const ClinvarTab = ({
  report,
  onOpen,
}: {
  report: GeneReport;
  onOpen: (detail: ReportDetail) => void;
}) => {
  const [clinvarSearch, setClinvarSearch] = useState("");
  const rows = getClinvarRows(report.clinvar.items ?? []);
  const visibleClinvarRows = rows.filter((row) =>
    row.search
      .toLocaleLowerCase("ru")
      .includes(clinvarSearch.toLocaleLowerCase("ru")),
  );
  return (
    <>
      <SectionHeading title="Классификации ClinVar" />
      {rows.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          {report.clinvar.status === "unavailable"
            ? "Данные ClinVar не получены."
            : "Записей ClinVar нет."}
        </Typography>
      ) : (
        <Stack spacing={3}>
          <TextField
            label="Поиск"
            size="small"
            value={clinvarSearch}
            onChange={(event) => setClinvarSearch(event.target.value)}
            sx={{ maxWidth: 420 }}
          />
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ display: { xs: "block", sm: "none" }, mt: -1 }}
          >
            Таблицы можно прокручивать по горизонтали.
          </Typography>
          {visibleClinvarRows.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              Совпадений нет.
            </Typography>
          ) : (
            clinvarCategories.map(({ key, title }) => {
              const rows = visibleClinvarRows.filter(
                (row) =>
                  row.detail.kind === "clinvar" &&
                  row.detail.item.category === key,
              );
              return rows.length === 0 ? null : (
                <Box key={key}>
                  <Stack
                    direction="row"
                    sx={{ mb: 1.5, gap: 1, alignItems: "center" }}
                  >
                    <Typography
                      component="h3"
                      variant="subtitle1"
                      sx={{ fontWeight: 700 }}
                    >
                      {title}
                    </Typography>
                    <Chip size="small" label={rows.length} variant="outlined" />
                  </Stack>
                  <ResultsTable
                    headers={[
                      "Ген",
                      "Генотип",
                      key === "drug_response"
                        ? "Ответ на препарат"
                        : "Заболевание или признак",
                      "Заключение источника",
                      "Статус проверки",
                    ]}
                    rows={rows}
                    onOpen={onOpen}
                    emptyLabel="Нет записей."
                    hideSearch
                    tableLabel={`${title} ClinVar`}
                  />
                </Box>
              );
            })
          )}
        </Stack>
      )}
    </>
  );
};
