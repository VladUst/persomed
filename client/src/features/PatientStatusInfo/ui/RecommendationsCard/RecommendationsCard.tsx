import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import PencilIcon from "@/shared/assets/icons/pencil.svg";

const data: PatientStatusInfo = [
  {
    text: "Take Omega 3",
    label: "1000 mg/day",
  },
  {
    text: "Alpha-lipoic acid",
    label: "600 mg/day",
  },
  {
    text: "Magnesium",
    label: "400 mg/day",
  },
  {
    text: "Limit sugar intake",
  },
  {
    text: "Regular aerobic exercise",
  },
];

interface RecommendationsCardProps {
  className?: string;
}

export const RecommendationsCard = (props: RecommendationsCardProps) => {
  const { className } = props;
  return (
    <PatientStatusCard
      icon={PencilIcon}
      id="7"
      title="Recommendations"
      className={className}
      variant={PatientStatusCardVariant.GREEN}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
