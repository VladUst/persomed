import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./OtherDocs.module.scss";

const otherDocsRows: GridRowsProp = [
  {
    id: "1",
    name: "Генетический профиль",
    type: "Генетика",
    date: "2023-12-01",
  },
  {
    id: "2",
    name: "Справка о госпитализации",
    type: "Справка",
    date: "2023-11-15",
  },
  {
    id: "3",
    name: "Выписка из стационара",
    type: "Выписка",
    date: "2024-01-20",
  },
];

const otherDocsColumns: GridColDef[] = [
  { field: "name", headerName: "Название документа", flex: 1 },
  { field: "type", headerName: "Тип", width: 150 },
  { field: "date", headerName: "Дата", width: 150 },
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
      <Divider className={cls.title}>Другие документы</Divider>
      <MedicalTable
        className={className}
        columns={otherDocsColumns}
        rows={otherDocsRows}
        handleClick={handleClick}
      />
    </>
  );
};
