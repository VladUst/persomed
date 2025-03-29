import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import SearchIcon from "@/shared/assets/icons/search.svg";

const data: PatientStatusInfo = [
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
    <PatientStatusCard
      icon={SearchIcon}
      id="suspicions"
      title="Подозрения"
      className={className}
      variant={PatientStatusCardVariant.RED}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
