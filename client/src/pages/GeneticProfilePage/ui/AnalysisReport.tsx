import { useRef, useState, type ReactNode } from "react";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Chip from "@mui/material/Chip";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import type { GeneReport } from "../api/genes";
import type {
  ClinvarItem,
  EvidenceRef,
  Finding,
  GenotypeRuleItem,
  PolygenicScoreItem,
} from "../model/report";
import { formatNumber, resultStatus, stabilityQuality } from "../model/report";
import { ReportDetailDialog, type ReportDetail } from "./ReportDetailDialog";

interface TableRowData {
  id: string;
  cells: ReactNode[];
  search: string;
  detail: ReportDetail;
}

const clinvarCategories: Array<{
  key: ClinvarItem["category"];
  title: string;
}> = [
  { key: "candidate", title: "Кандидаты для проверки" },
  { key: "conflicting", title: "Спорные заключения" },
  { key: "uncertain", title: "Неопределённая значимость" },
  { key: "association", title: "Ассоциации" },
  { key: "drug_response", title: "Фармакогенетика" },
];

const pgsColumnHints: Record<string, string> = {
  Признак:
    "Заболевание или показатель, для которого создана модель. Число SNP в скобках показывает, сколько генетических позиций входит в модель, а не сколько изменений найдено у пациента. Для одного признака в отчёте может быть несколько моделей.",
  Модель:
    "Номер модели в PGS Catalog. Разные модели одного признака используют разные наборы SNP и разные веса для расчёта балла. Откройте строку таблицы, чтобы перейти к источнику именно этой модели.",
  Оценка:
    "«Оценено» означает, что балл по этой модели удалось рассчитать. При этом часть SNP могла отсутствовать в VCF, поэтому рядом нужно проверить измеренное покрытие. «Не оценено» означает, что расчёт не выполнен, например из-за недостатка найденных SNP или неподходящего файла весов. Точная причина указана в подробностях модели.",
  "EUR-перцентиль":
    "Положение рассчитанного балла среди баллов EUR-образцов в референсной выборке. Например, 80-й перцентиль означает, что балл пациента выше примерно 80% баллов в этой выборке. Это не означает 80% вероятности заболевания. «Не рассчитан» означает, что сравнение с выборкой выполнить не удалось; причина есть в подробностях модели.",
  "Измеренное покрытие":
    "Доля SNP модели, для которых в VCF найден генотип пациента и подтверждено совпадение координаты и аллелей. Например, 40% означает, что напрямую учтены 40 из 100 SNP модели. SNP, для которых вместо генотипа подставлено среднее значение по популяции, в этот процент не входят.",
  Устойчивость:
    "Показывает, насколько результат зависит от SNP модели, отсутствующих в VCF. Сервер сравнивает на EUR-выборке балл по найденным SNP с баллом по полной модели. «Хорошая» означает, что баллы хорошо согласуются и возможный диапазон перцентиля остаётся в одной категории; «ограниченная» и «низкая» указывают на менее надёжное совпадение. Прочерк означает, что сравнение выполнить не удалось.",
};

const sourceDetails = (url: string) => {
  if (url.includes("myvariant.info")) {
    return {
      name: "MyVariant.info",
      description:
        "Аннотации вариантов VCF; через этот ресурс получаются записи ClinVar для сопоставления с генотипом.",
    };
  }
  if (url.includes("pgscatalog.org")) {
    return {
      name: "PGS Catalog",
      description:
        "Каталог полигенных моделей: описания признаков и файлы весов SNP для расчёта оценок.",
    };
  }
  if (url.includes("internationalgenome.org")) {
    return {
      name: "1000 Genomes Project",
      description:
        "Публичные генотипы, на основе которых подготовлена EUR-выборка для сравнения полигенного балла.",
    };
  }
  return {
    name: url,
    description: "Дополнительный источник, указанный в отчёте.",
  };
};

const ResultsTable = ({
  headers,
  rows,
  emptyLabel,
  onOpen,
  headerHints,
  hideSearch = false,
  tableLabel = "Результаты генетического анализа",
}: {
  headers: string[];
  rows: TableRowData[];
  emptyLabel: string;
  onOpen: (detail: ReportDetail) => void;
  headerHints?: Record<string, string>;
  hideSearch?: boolean;
  tableLabel?: string;
}) => {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const filtered = rows.filter((row) =>
    row.search.toLocaleLowerCase("ru").includes(search.toLocaleLowerCase("ru")),
  );
  const visiblePage = Math.min(
    page,
    Math.max(0, Math.ceil(filtered.length / pageSize) - 1),
  );

  return (
    <Stack spacing={2}>
      {!hideSearch && (
        <TextField
          label="Поиск"
          size="small"
          value={search}
          onChange={(event) => {
            setSearch(event.target.value);
            setPage(0);
          }}
          sx={{ maxWidth: 420 }}
        />
      )}
      {filtered.length === 0 ? (
        <Typography variant="body2" color="text.secondary">
          {search ? "Совпадений нет." : emptyLabel}
        </Typography>
      ) : (
        <Paper variant="outlined" sx={{ borderRadius: 2, overflow: "hidden" }}>
          <TableContainer
            role="region"
            aria-label={`Прокручиваемая таблица: ${tableLabel}`}
            tabIndex={0}
          >
            <Table size="small" aria-label={tableLabel}>
              <TableHead>
                <TableRow sx={{ bgcolor: "action.hover" }}>
                  {headers.map((header) => (
                    <TableCell key={header} sx={{ fontWeight: 700 }}>
                      <Stack
                        direction="row"
                        sx={{ alignItems: "center", gap: 0.5 }}
                      >
                        {header}
                        {headerHints?.[header] && (
                          <Tooltip
                            title={headerHints[header]}
                            arrow
                            describeChild
                            enterTouchDelay={0}
                            leaveTouchDelay={5000}
                            slotProps={{
                              tooltip: {
                                sx: {
                                  fontSize: "0.8125rem",
                                  lineHeight: 1.5,
                                  maxWidth: "min(380px, calc(100vw - 32px))",
                                  px: 1.25,
                                  py: 1,
                                },
                              },
                            }}
                          >
                            <IconButton
                              aria-label={`Пояснение к колонке «${header}»`}
                              sx={{ width: 44, height: 44, flexShrink: 0 }}
                            >
                              <InfoOutlinedIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )}
                      </Stack>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {filtered
                  .slice(visiblePage * pageSize, (visiblePage + 1) * pageSize)
                  .map((row) => (
                    <TableRow key={row.id} hover>
                      {row.cells.map((cell, index) => (
                        <TableCell key={index}>
                          {index === 0 ? (
                            <Button
                              sx={{ textAlign: "left", textTransform: "none" }}
                              onClick={() => onOpen(row.detail)}
                            >
                              {cell}
                            </Button>
                          ) : (
                            cell
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          {filtered.length > pageSize && (
            <TablePagination
              component="div"
              count={filtered.length}
              page={visiblePage}
              onPageChange={(_, next) => setPage(next)}
              rowsPerPage={pageSize}
              onRowsPerPageChange={(event) => {
                setPageSize(Number(event.target.value));
                setPage(0);
              }}
              rowsPerPageOptions={[10, 25, 50]}
              labelRowsPerPage="Строк на странице"
              labelDisplayedRows={({ from, to, count }) =>
                `${from}–${to} из ${count}`
              }
              getItemAriaLabel={(type) =>
                type === "previous"
                  ? "Предыдущая страница"
                  : "Следующая страница"
              }
            />
          )}
        </Paper>
      )}
    </Stack>
  );
};

const SectionHeading = ({ title }: { title: string }) => (
  <Typography component="h2" variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
    {title}
  </Typography>
);

export const AnalysisReport = ({ report }: { report: GeneReport }) => {
  const [tab, setTab] = useState(0);
  const [detail, setDetail] = useState<ReportDetail | null>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [clinvarSearch, setClinvarSearch] = useState("");
  const pgsTabRef = useRef<HTMLDivElement>(null);
  const clinvarItems = report.clinvar.items ?? [];
  const ruleItems = report.genotype_rules.items ?? [];
  const pgsItems = report.polygenic_scores.items ?? [];
  const openDetail = (nextDetail: ReportDetail) => {
    setDetail(nextDetail);
    setDetailOpen(true);
  };
  const showAllPgs = () => {
    setTab(3);
    requestAnimationFrame(() => pgsTabRef.current?.focus());
  };
  const qualityMetrics = [
    {
      label: "Число всех вариантов в файле",
      value: report.quality.total_records,
      explanation:
        "Всего вариантов, перечисленных в файле генетического профиля VCF. В это число входят и варианты с генотипом 0|0, у которых альтернативный аллель у пациента не выявлен.",
    },
    {
      label: "Число вариантов, учтённых при анализе",
      value: report.quality.usable_records,
      explanation:
        "Число вариантов, для которых удалось определить генотип пациента из двух аллелей, например 0|0 или 0|1. Они переданы в анализ.",
    },
    {
      label: "Число вариантов, пропущенных при анализе",
      value: report.quality.skipped_records,
      explanation:
        "Число вариантов, которые не вошли в анализ: генотип отсутствует, содержит не два аллеля или указывает на аллель, не перечисленный в VCF.",
    },
    {
      label: "Число вариантов с альтернативным аллелем",
      value: report.quality.alt_records,
      explanation:
        "В этих вариантах генотип пациента содержит хотя бы один альтернативный аллель, например 0|1 или 1|1.",
    },
    {
      label: "Аннотаций ClinVar без совпадения",
      value: report.quality.unmatched_annotations,
      explanation:
        "Число аннотаций ClinVar, для которых не найден ровно один соответствующий вариант в VCF. При сопоставлении проверяются координата, аллели и генотип пациента. Такие аннотации не включены в таблицы ClinVar.",
    },
  ];

  const openEvidence = (ref: EvidenceRef) => {
    if (ref.section === "clinvar") {
      const item = clinvarItems.find((entry) => entry.id === ref.item_id);
      if (item) openDetail({ kind: "clinvar", item });
    } else if (ref.section === "genotype_rules") {
      const item = ruleItems.find((entry) => entry.id === ref.item_id);
      if (item) openDetail({ kind: "rule", item });
    } else {
      const item = pgsItems.find((entry) => entry.pgs_id === ref.item_id);
      if (item) openDetail({ kind: "pgs", item });
    }
  };

  const clinvarRows: TableRowData[] = clinvarItems.map((item: ClinvarItem) => ({
    id: item.id,
    cells: [
      item.genes.join(", ") || "Вариант",
      item.conditions.join("; "),
      item.genotype,
      item.review_status ?? "Не указан",
    ],
    search: [
      item.genes,
      item.conditions,
      item.variant.rsid,
      item.accession,
      item.significance.original,
    ].join(" "),
    detail: { kind: "clinvar", item },
  }));
  const visibleClinvarRows = clinvarRows.filter((row) =>
    row.search
      .toLocaleLowerCase("ru")
      .includes(clinvarSearch.toLocaleLowerCase("ru")),
  );
  const ruleRows: TableRowData[] = ruleItems.map((item: GenotypeRuleItem) => ({
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
  const pgsRows: TableRowData[] = pgsItems.map((item: PolygenicScoreItem) => ({
    id: item.pgs_id,
    cells: [
      item.trait,
      item.pgs_id,
      resultStatus(item.status),
      item.reference_comparison.percentile == null
        ? "Не рассчитан"
        : `${formatNumber(item.reference_comparison.percentile)}-й`,
      item.coverage ? `${formatNumber(item.coverage.measured_percent)}%` : "—",
      stabilityQuality(item.stability?.quality),
    ],
    search: [
      item.trait,
      item.pgs_id,
      item.reference_comparison.category_label,
      item.reason?.message,
    ].join(" "),
    detail: { kind: "pgs", item },
  }));

  return (
    <Stack spacing={2}>
      <Paper variant="outlined" sx={{ borderRadius: 3, overflow: "hidden" }}>
        <Tabs
          value={tab}
          onChange={(_, value: number) => setTab(value)}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="Разделы генетического отчёта"
        >
          <Tab label="Обзор" />
          <Tab label={`ClinVar (${clinvarItems.length})`} />
          <Tab label={`Генотипы (${ruleItems.length})`} />
          <Tab
            ref={pgsTabRef}
            label={`Полигенные оценки (${pgsItems.length})`}
          />
          <Tab label="Источники" />
        </Tabs>
        <Divider />
        <Box sx={{ p: { xs: 2, md: 3 } }} role="tabpanel">
          {tab === 0 && (
            <Stack spacing={3}>
              <Box>
                <Typography
                  component="h2"
                  variant="h6"
                  sx={{ fontWeight: 700, mb: 1 }}
                >
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
                          <Typography
                            variant="subtitle1"
                            sx={{ fontWeight: 700 }}
                          >
                            {finding.condition}
                          </Typography>
                          <Typography variant="body2" color="primary.main">
                            {finding.role}
                          </Typography>
                          <Typography variant="body2">
                            {finding.interpretation}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Вопрос врачу:</strong>{" "}
                            {finding.clinical_question}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Следующий шаг:</strong> {finding.next_step}
                          </Typography>
                          <Stack
                            direction="row"
                            sx={{ gap: 1, flexWrap: "wrap" }}
                          >
                            <Button
                              size="small"
                              onClick={() =>
                                openDetail({ kind: "finding", item: finding })
                              }
                            >
                              Подробнее
                            </Button>
                            {finding.evidence_refs.map((ref) => (
                              <Button
                                key={`${ref.section}-${ref.item_id}`}
                                size="small"
                                variant="outlined"
                                onClick={() => openEvidence(ref)}
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
                <Typography
                  component="h2"
                  variant="h6"
                  sx={{ fontWeight: 700, mb: 1 }}
                >
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
                        <Typography
                          variant="subtitle2"
                          sx={{ fontWeight: 700 }}
                        >
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
                            onClick={() => openDetail({ kind: "pgs", item })}
                          >
                            Детали модели
                          </Button>
                        )}
                      </Paper>
                    );
                  })}
                </Box>
                <Button onClick={showAllPgs} sx={{ mb: 2 }}>
                  Все оценки ({pgsItems.length})
                </Button>
              </Box>
            </Stack>
          )}
          {tab === 1 && (
            <>
              <SectionHeading title="Классификации ClinVar" />
              {clinvarRows.length === 0 ? (
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
                            <Chip
                              size="small"
                              label={rows.length}
                              variant="outlined"
                            />
                          </Stack>
                          <ResultsTable
                            headers={[
                              "Ген",
                              "Состояние",
                              "Генотип",
                              "Статус проверки",
                            ]}
                            rows={rows}
                            onOpen={openDetail}
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
          )}
          {tab === 2 && (
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
                rows={ruleRows}
                onOpen={openDetail}
                emptyLabel="Правила отсутствуют в отчёте."
              />
            </>
          )}
          {tab === 3 && (
            <>
              <SectionHeading title="Полигенные оценки" />
              <ResultsTable
                headers={[
                  "Признак",
                  "Модель",
                  "Оценка",
                  "EUR-перцентиль",
                  "Измеренное покрытие",
                  "Устойчивость",
                ]}
                headerHints={pgsColumnHints}
                rows={pgsRows}
                onOpen={openDetail}
                emptyLabel="Полигенные модели отсутствуют в отчёте."
              />
            </>
          )}
          {tab === 4 && (
            <Stack spacing={3}>
              <Box>
                <Typography
                  component="h2"
                  variant="h6"
                  sx={{ fontWeight: 700 }}
                >
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
                <Typography
                  component="h2"
                  variant="h6"
                  sx={{ fontWeight: 700 }}
                >
                  Источники данных
                </Typography>
                {report.provenance.sources.length === 0 ? (
                  <Typography
                    variant="body2"
                    color="text.secondary"
                    sx={{ mt: 1.5 }}
                  >
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
          )}
        </Box>
      </Paper>
      <ReportDetailDialog
        detail={detail}
        open={detailOpen}
        onClose={() => setDetailOpen(false)}
      />
    </Stack>
  );
};
