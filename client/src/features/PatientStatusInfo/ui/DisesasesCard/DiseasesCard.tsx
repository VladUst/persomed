import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import HealthIcon from "@/shared/assets/icons/health.svg";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";

const data: PatientStatusInfo = [
  {
    text: "ОРВИ",
    label: "J00-J02",
  },
  {
    text: "Артериальная гипертензия",
    label: "I11",
  },
  {
    text: "Сердечная недостаточность",
    label: "I50.0",
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
      id="diseases"
      title="Заболевания"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
