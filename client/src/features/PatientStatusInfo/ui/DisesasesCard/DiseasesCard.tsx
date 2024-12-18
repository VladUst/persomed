import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import HealthIcon from "@/shared/assets/icons/health.svg";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";

const data: PatientStatusInfo = [
  {
    text: "Arterial hypertension",
    label: "I11",
  },
  {
    text: "Heart failure",
    label: "I50.0",
  },
  {
    text: "Acute respiratory viral infection",
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
      id="2"
      title="Diseases"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
