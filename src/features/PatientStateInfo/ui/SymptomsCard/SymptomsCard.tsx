import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Повышенный уровень сахара",
  },
  {
    text: "Повышенная глюкоза крови",
  },
];

interface SymptomsCardProps {
  className?: string;
}

export const SymptomsCard = (props: SymptomsCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Симптомы"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
