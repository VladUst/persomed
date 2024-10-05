import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Сахарный диабет",
    label: "E10",
  },
];

interface SuspicionsCardProps {
  className?: string;
}

export const SuspicionsCard = (props: SuspicionsCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Подозрения"
      className={className}
      variant={PatientStateCardVariant.RED}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
