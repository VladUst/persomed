import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Принимать витамины D3 и OMEGA 6",
    label: "1 доз./ден.",
  },
  {
    text: "Ограничить употребление сахара",
  },
];

interface RecommendationsCardProps {
  className?: string;
}

export const RecommendationsCard = (props: RecommendationsCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Рекомендации"
      className={className}
      variant={PatientStateCardVariant.GREEN}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
