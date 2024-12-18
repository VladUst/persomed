import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./OtherDocs.module.scss";

const otherDocsRows: GridRowsProp = [
  {
    id: "1",
    name: "Genetic Profile",
    type: "Genetics",
    date: "2023-12-01",
  },
  {
    id: "2",
    name: "Hospitalization Certificate",
    type: "Certificate",
    date: "2023-11-15",
  },
  {
    id: "3",
    name: "Hospital Discharge Summary",
    type: "Discharge",
    date: "2024-01-20",
  },
];

const otherDocsColumns: GridColDef[] = [
  { field: "name", headerName: "Document Name", flex: 1 },
  { field: "type", headerName: "Type", width: 150 },
  { field: "date", headerName: "Date", width: 150 },
];

interface OtherDocsProps {
  className?: string;
}

export const OtherDocs = (props: OtherDocsProps) => {
  const { className } = props;
  const handleClick = (id: string) => {
    console.log("History clicked:", id);
  };

  return (
    <>
      <Divider className={cls.title}>Other documents</Divider>
      <MedicalTable
        className={className}
        columns={otherDocsColumns}
        rows={otherDocsRows}
        handleClick={handleClick}
      />
    </>
  );
};
