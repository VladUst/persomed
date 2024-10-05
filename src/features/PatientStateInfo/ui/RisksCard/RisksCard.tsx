import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Целевое АД не достигнуто",
  },
  {
    text: "Артериальная гипертензия",
  },
  {
    text: "Наличие сердечно-сосудистых заболеваний",
  },
  {
    text: "Увеличение ЧСС в покое",
  },
];

interface RisksCardProps {
  className?: string;
}

export const RisksCard = (props: RisksCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Факторы риска"
      className={className}
      variant={PatientStateCardVariant.RED}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};