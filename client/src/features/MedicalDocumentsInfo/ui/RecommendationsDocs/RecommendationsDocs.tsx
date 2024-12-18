import { MedicalTable } from "@/entities/MedicalTable/ui/MedicalTable";
import { Divider } from "@mui/material";
import type { GridColDef, GridRowsProp } from "@mui/x-data-grid";
import cls from "./RecommendationsDocs.module.scss";

const recommendationsRows: GridRowsProp = [
  {
    id: "1",
    name: "Reduce consumption of fatty foods",
    type: "Recommendation",
    specialty: "Therapist",
    date: "2024-03-01",
  },
  {
    id: "2",
    name: "Medication: Lisinopril",
    type: "Prescription",
    specialty: "Cardiologist",
    date: "2024-03-05",
  },
  {
    id: "3",
    name: "Daily walking for 30 minutes",
    type: "Recommendation",
    specialty: "Cardiologist",
    date: "2024-03-10",
  },
];

const recommendationsColumns: GridColDef[] = [
  { field: "name", headerName: "Recommendation Name", flex: 1 },
  { field: "type", headerName: "Type", width: 200 },
  { field: "specialty", headerName: "Doctor Specialty", width: 200 },
  { field: "date", headerName: "Date", width: 150 },
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
      <Divider className={cls.title}>
        Recommendations and appointments of doctors
      </Divider>
      <MedicalTable
        className={className}
        columns={recommendationsColumns}
        rows={recommendationsRows}
        handleClick={handleClick}
      />
    </>
  );
};
