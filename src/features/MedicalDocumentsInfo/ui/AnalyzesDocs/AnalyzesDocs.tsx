import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./AnalyzesDocs.module.scss";

const analyzesRows: GridRowsProp = [
  {
    id: "1",
    name: "Общий анализ крови",
    type: "Лабораторный",
    date: "2024-01-15",
  },
  {
    id: "2",
    name: "Биохимический анализ крови",
    type: "Лабораторный",
    date: "2024-01-20",
  },
  { id: "3", name: "ЭКГ", type: "Диагностический", date: "2024-02-01" },
  { id: "4", name: "УЗИ сердца", type: "Диагностический", date: "2024-02-10" },
];

const analyzesColumns: GridColDef[] = [
  { field: "name", headerName: "Название исследования", flex: 1 },
  { field: "type", headerName: "Тип", width: 200 },
  { field: "date", headerName: "Дата проведения", width: 150 },
];

interface AnalyzesDocsProps {
  className?: string;
}

export const AnalyzesDocs = (props: AnalyzesDocsProps) => {
  const { className } = props;
  const handleClick = (id: string) => {
    console.log("Analyzes clicked:", id);
  };

  return (
    <>
      <Divider className={cls.title}>
        Лабораторные и диагностические исследования
      </Divider>
      <MedicalTable
        className={className}
        columns={analyzesColumns}
        rows={analyzesRows}
        handleClick={handleClick}
      />
    </>
  );
};
