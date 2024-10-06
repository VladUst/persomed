import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import PencilIcon from "@/shared/assets/icons/pencil.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStateInfo = [
  {
    text: "Принимать Омега 3",
    label: "1000 мг./ден.",
  },
  {
    text: "Альфа-липоевая кислота",
    label: "600 мг./ден.",
  },
  {
    text: "Магний",
    label: "400 мг./ден.",
  },
  {
    text: "Ограничить употребление сахара",
  },
  {
    text: "Регулярные аэробные нагрузки",
  },
];

interface RecommendationsCardProps {
  className?: string;
}

export const RecommendationsCard = (props: RecommendationsCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      icon={PencilIcon}
      link={getRouteDigitalProfile()}
      title="Рекомендации"
      className={className}
      variant={PatientStateCardVariant.GREEN}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
