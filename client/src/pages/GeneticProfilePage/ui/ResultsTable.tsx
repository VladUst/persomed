import { useState, type ReactNode } from "react";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TextField from "@mui/material/TextField";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import type { ReportDetail } from "../model/report";

export interface TableRowData {
  id: string;
  cells: ReactNode[];
  search: string;
  detail: ReportDetail;
}

export const ResultsTable = ({
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
              labelRowsPerPage="Строк в таблице"
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
