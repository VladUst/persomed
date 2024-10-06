import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import { getRouteDigitalProfile } from "@/shared/const/router";
import HealthIcon from "@/shared/assets/icons/health.svg";

const data: PatientStateInfo = [
  {
    text: "Артериальная гипертензия",
    label: "I11",
  },
  {
    text: "Сердечная недостаточность",
    label: "I50.0",
  },
  {
    text: "ОРВИ",
    label: "J00-J02",
  },
];

interface DiseasesCardProps {
  className?: string;
}

export const DiseasesCard = (props: DiseasesCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      icon={HealthIcon}
      link={getRouteDigitalProfile()}
      title="Заболевания"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
