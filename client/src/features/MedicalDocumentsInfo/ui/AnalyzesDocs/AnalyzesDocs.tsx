import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./AnalyzesDocs.module.scss";

const analyzesRows: GridRowsProp = [
  {
    id: "1",
    name: "Complete Blood Count",
    type: "Laboratory",
    date: "2024-01-15",
  },
  {
    id: "2",
    name: "Biochemical Blood Test",
    type: "Laboratory",
    date: "2024-01-20",
  },
  { id: "3", name: "ECG", type: "Diagnostic", date: "2024-02-01" },
  { id: "4", name: "Heart Ultrasound", type: "Diagnostic", date: "2024-02-10" },
];

const analyzesColumns: GridColDef[] = [
  { field: "name", headerName: "Test Name", flex: 1 },
  { field: "type", headerName: "Type", width: 200 },
  { field: "date", headerName: "Date Conducted", width: 150 },
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
      <Divider className={cls.title}>Laboratory and diagnostic studies</Divider>
      <MedicalTable
        className={className}
        columns={analyzesColumns}
        rows={analyzesRows}
        handleClick={handleClick}
      />
    </>
  );
};
