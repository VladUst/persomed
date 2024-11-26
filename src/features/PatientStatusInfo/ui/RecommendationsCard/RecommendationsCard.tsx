import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import PencilIcon from "@/shared/assets/icons/pencil.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStatusInfo = [
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
    <PatientStatusCard
      icon={PencilIcon}
      link={getRouteDigitalProfile()}
      title="Рекомендации"
      className={className}
      variant={PatientStatusCardVariant.GREEN}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
