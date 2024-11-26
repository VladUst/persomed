import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import EyeIcon from "@/shared/assets/icons/eye.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStatusInfo = [
  {
    text: "Повышенная глюкоза крови",
  },
  {
    text: "Высокие уровни кетонов",
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
      link={getRouteDigitalProfile()}
      title="Симптомы"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
