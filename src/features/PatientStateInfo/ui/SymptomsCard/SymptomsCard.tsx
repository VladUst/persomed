import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import EyeIcon from "@/shared/assets/icons/eye.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStateInfo = [
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
    <PatientStateCard
      icon={EyeIcon}
      link={getRouteDigitalProfile()}
      title="Симптомы"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
