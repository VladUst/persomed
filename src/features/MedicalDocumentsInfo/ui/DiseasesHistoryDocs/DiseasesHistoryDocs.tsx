import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./DiseasesHistoryDocs.module.scss";

const historyRows: GridRowsProp = [
  {
    id: "1",
    icdCode: "-",
    name: "Подозрение на диабет",
    type: "Анамнез",
    date: "2024-07-17",
  },
  {
    id: "2",
    icdCode: "J00-J02",
    name: "ОРВИ",
    type: "Обычное",
    date: "2024-02-09",
  },
  {
    id: "3",
    icdCode: "I11",
    name: "Артериальная гипертензия",
    type: "Хроническое",
    date: "2023-01-15",
  },
  {
    id: "4",
    icdCode: "I50.9",
    name: "Сердечная недостаточность",
    type: "Хроническое",
    date: "2023-02-10",
  },
];

const historyColumns: GridColDef[] = [
  { field: "icdCode", headerName: "Код МКБ-10", width: 150 },
  { field: "name", headerName: "Название диагноза", flex: 1 },
  { field: "type", headerName: "Тип", width: 150 },
  { field: "date", headerName: "Дата постановки", width: 150 },
];

interface DiseasesHistoryDocsProps {
  className?: string;
}

export const DiseasesHistoryDocs = (props: DiseasesHistoryDocsProps) => {
  const { className } = props;
  const handleClick = (id: string) => {
    console.log("History clicked:", id);
  };

  return (
    <>
      <Divider className={cls.title}>История болезней</Divider>
      <MedicalTable
        className={className}
        columns={historyColumns}
        rows={historyRows}
        handleClick={handleClick}
      />
    </>
  );
};
