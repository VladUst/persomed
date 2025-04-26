import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import EyeIcon from "@/shared/assets/icons/eye.svg";

const data: PatientStatusInfo = [
  {
    text: "Сильная жажда",
  },
  {
    text: "Полифагия",
  },
  {
    text: "Потеря веса",
  },
  {
    text: "Слабость",
  },
];

interface SymptomsCardProps {
  className?: string;
}

export const SymptomsCard = (props: SymptomsCardProps) => {
  const { className } = props;
  return (
    <PatientStatusCard
      icon={EyeIcon}
      id="symptoms"
      title="Симптомы"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
