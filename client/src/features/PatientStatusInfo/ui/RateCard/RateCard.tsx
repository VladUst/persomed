import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import WarnIcon from "@/shared/assets/icons/warning.svg";

const data: PatientStatusInfo = [
  {
    text: "Сердечно-сосудистые заболевания",
    label: "Высокие",
    labelColor: "#E90711",
  },
  {
    text: "Заболевания системы пищеварения",
    label: "Средние",
    labelColor: "#ECB404",
  },
  {
    text: "Заболевания органов дыхания",
    label: "Низкие",
    labelColor: "#53D006",
  },
  {
    text: "Заболевания эндокринной системы",
    label: "Низкие",
    labelColor: "#53D006",
  },
  {
    text: "Заболевания почек и мочевыделительной системы",
    label: "Низкие",
    labelColor: "#53D006",
  },
  {
    text: "Заболевания опорно-двигательного аппарата",
    label: "Неизвестно",
  },
  {
    text: "Заболевания кожи и волосяных покровов",
    label: "Неизвестно",
  },
];

interface RateCardProps {
  className?: string;
}

export const RateCard = (props: RateCardProps) => {
  const { className } = props;
  return (
    <PatientStatusCard
      icon={WarnIcon}
      id="rates"
      title="Оценка рисков"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
