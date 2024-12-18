import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import FireIcon from "@/shared/assets/icons/fire.svg";

const data: PatientStatusInfo = [
  {
    text: "High risk of heart attack",
  },
  {
    text: "Target blood pressure not reached",
  },
  {
    text: "Target heart rate not reached",
  },
  {
    text: "Arterial hypertension",
  },
  {
    text: "Heart failure",
  },
];

interface RisksCardProps {
  className?: string;
}

export const RisksCard = (props: RisksCardProps) => {
  const { className } = props;
  return (
    <PatientStatusCard
      icon={FireIcon}
      id="5"
      title="Risk factors"
      className={className}
      variant={PatientStatusCardVariant.RED}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
