import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./RecommendationsDocs.module.scss";

const recommendationsRows: GridRowsProp = [
  {
    id: "1",
    name: "Снижение потребления жирной пищи",
    type: "Рекомендация",
    specialty: "Терапевт",
    date: "2024-03-01",
  },
  {
    id: "2",
    name: "Препарат: Лизиноприл",
    type: "Назначение",
    specialty: "Кардиолог",
    date: "2024-03-05",
  },
  {
    id: "3",
    name: "Ежедневная ходьба 30 минут",
    type: "Рекомендация",
    specialty: "Кардиолог",
    date: "2024-03-10",
  },
];

const recommendationsColumns: GridColDef[] = [
  { field: "name", headerName: "Название рекомендации", flex: 1 },
  { field: "type", headerName: "Тип", width: 200 },
  { field: "specialty", headerName: "Специальность врача", width: 200 },
  { field: "date", headerName: "Дата", width: 150 },
];

interface RecommendationsDocsProps {
  className?: string;
}

export const RecommendationsDocs = (props: RecommendationsDocsProps) => {
  const { className } = props;
  const handleClick = (id: string) => {
    console.log("History clicked:", id);
  };

  return (
    <>
      <Divider className={cls.title}>Рекомендации и назначения врачей</Divider>
      <MedicalTable
        className={className}
        columns={recommendationsColumns}
        rows={recommendationsRows}
        handleClick={handleClick}
      />
    </>
  );
};
