import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { getRouteDigitalProfile } from "@/shared/const/router";
import HealthIcon from "@/shared/assets/icons/health.svg";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";

const data: PatientStatusInfo = [
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
    <PatientStatusCard
      icon={HealthIcon}
      link={getRouteDigitalProfile()}
      title="Заболевания"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
