import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import type { GeneReport } from "../api/genes";
import { getQualityMetrics } from "./qualityMetrics";
import { formatNumber } from "./reportFormatting";
import { sourceDetails } from "./sourceDescriptions";

export const ReportMetadataTab = ({ report }: { report: GeneReport }) => {
  const qualityMetrics = getQualityMetrics(report.quality);
  return (
    <Stack spacing={3}>
      <Box>
        <Typography component="h2" variant="h6" sx={{ fontWeight: 700 }}>
          Параметры анализа
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
            mt: 1.5,
          }}
        >
          {qualityMetrics.map(({ label, value, explanation }) => (
            <Paper
              key={label}
              variant="outlined"
              sx={{ p: 2, borderRadius: 2 }}
            >
              <Typography
                component="p"
                variant="h6"
                sx={{
                  fontWeight: 700,
                  fontVariantNumeric: "tabular-nums",
                }}
              >
                {formatNumber(value, 0)}
              </Typography>
              <Stack
                direction="row"
                sx={{
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 1,
                }}
              >
                <Typography variant="body2" color="text.secondary">
                  {label}
                </Typography>
                <Tooltip
                  title={explanation}
                  arrow
                  describeChild
                  enterTouchDelay={0}
                  leaveTouchDelay={5000}
                  slotProps={{
                    tooltip: {
                      sx: {
                        fontSize: "0.8125rem",
                        lineHeight: 1.5,
                        maxWidth: 360,
                        px: 1.25,
                        py: 1,
                      },
                    },
                  }}
                >
                  <IconButton
                    aria-label={`Пояснение: ${label}`}
                    sx={{ width: 44, height: 44, flexShrink: 0 }}
                  >
                    <InfoOutlinedIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              </Stack>
            </Paper>
          ))}
        </Box>
      </Box>
      <Box>
        <Typography component="h2" variant="h6" sx={{ fontWeight: 700 }}>
          Источники данных
        </Typography>
        {report.provenance.sources.length === 0 ? (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1.5 }}>
            Источники не указаны в отчёте.
          </Typography>
        ) : (
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: {
                xs: "1fr",
                md: "repeat(3, minmax(0, 1fr))",
              },
              gap: 2,
              mt: 1.5,
            }}
          >
            {report.provenance.sources.map((source) => {
              const { name, description } = sourceDetails(source.url);
              return (
                <Paper
                  key={source.url}
                  variant="outlined"
                  sx={{ p: 2.5, borderRadius: 2, minWidth: 0 }}
                >
                  <Stack spacing={1.5} sx={{ height: "100%" }}>
                    <Typography
                      component="h3"
                      variant="subtitle1"
                      sx={{ fontWeight: 700, overflowWrap: "anywhere" }}
                    >
                      {name}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ flexGrow: 1 }}
                    >
                      {description}
                    </Typography>
                    <Link
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      aria-label={`Открыть ${name} в новой вкладке`}
                      sx={{ alignSelf: "flex-start" }}
                    >
                      Открыть источник ↗
                    </Link>
                  </Stack>
                </Paper>
              );
            })}
          </Box>
        )}
      </Box>
    </Stack>
  );
};
