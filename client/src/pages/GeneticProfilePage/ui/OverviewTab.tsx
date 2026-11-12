import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import type { GeneReport } from "../api/genes";
import type { EvidenceRef, Finding, ReportDetail } from "../model/report";
import { formatNumber } from "./reportFormatting";

export const OverviewTab = ({
  report,
  onOpen,
  onOpenEvidence,
  onShowAllPgs,
}: {
  report: GeneReport;
  onOpen: (detail: ReportDetail) => void;
  onOpenEvidence: (ref: EvidenceRef) => void;
  onShowAllPgs: () => void;
}) => {
  const pgsItems = report.polygenic_scores.items ?? [];
  return (
    <Stack spacing={3}>
      <Box>
        <Typography component="h2" variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
          Основные находки
        </Typography>
        {report.summary.findings.length === 0 ? (
          <Typography variant="body2" color="text.secondary">
            Приоритетных находок нет.
          </Typography>
        ) : (
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: {
                xs: "1fr",
                md: "repeat(2, minmax(0, 1fr))",
              },
              gap: 2,
            }}
          >
            {report.summary.findings.map((finding: Finding) => (
              <Paper
                key={finding.id}
                variant="outlined"
                sx={{
                  p: 2.5,
                  borderRadius: 2,
                  borderLeft: "4px solid",
                  borderLeftColor: "primary.main",
                }}
              >
                <Stack spacing={1.5}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
                    {finding.condition}
                  </Typography>
                  <Typography variant="body2" color="primary.main">
                    {finding.role}
                  </Typography>
                  <Typography variant="body2">
                    {finding.interpretation}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Вопрос врачу:</strong> {finding.clinical_question}
                  </Typography>
                  <Typography variant="body2">
                    <strong>Следующий шаг:</strong> {finding.next_step}
                  </Typography>
                  <Stack direction="row" sx={{ gap: 1, flexWrap: "wrap" }}>
                    <Button
                      size="small"
                      onClick={() => onOpen({ kind: "finding", item: finding })}
                    >
                      Подробнее
                    </Button>
                    {finding.evidence_refs.map((ref) => (
                      <Button
                        key={`${ref.section}-${ref.item_id}`}
                        size="small"
                        variant="outlined"
                        onClick={() => onOpenEvidence(ref)}
                      >
                        Доказательство
                      </Button>
                    ))}
                  </Stack>
                </Stack>
              </Paper>
            ))}
          </Box>
        )}
      </Box>
      <Box>
        <Typography component="h2" variant="h6" sx={{ fontWeight: 700, mb: 1 }}>
          Полигенные оценки
        </Typography>

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeat(2, minmax(0, 1fr))",
              lg: "repeat(3, minmax(0, 1fr))",
            },
            gap: 1.5,
          }}
        >
          {report.summary.polygenic_overview.map((entry) => {
            const item = pgsItems.find(
              (score) => score.pgs_id === entry.pgs_id,
            );
            return (
              <Paper
                key={entry.trait_id}
                variant="outlined"
                sx={{ p: 2, borderRadius: 2 }}
              >
                <Typography variant="subtitle2" sx={{ fontWeight: 700 }}>
                  {entry.trait}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {entry.pgs_id}
                </Typography>
                <Typography variant="body2" sx={{ my: 1 }}>
                  {item?.reference_comparison.percentile == null
                    ? "EUR-сравнение недоступно"
                    : `${formatNumber(item.reference_comparison.percentile)}-й перцентиль среди EUR-образцов`}
                </Typography>
                {item && (
                  <Button
                    size="small"
                    onClick={() => onOpen({ kind: "pgs", item })}
                  >
                    Детали модели
                  </Button>
                )}
              </Paper>
            );
          })}
        </Box>
        <Button onClick={onShowAllPgs} sx={{ mb: 2 }}>
          Все оценки ({pgsItems.length})
        </Button>
      </Box>
    </Stack>
  );
};
