import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import { getRouteDigitalProfile } from "@/shared/const/router";
import WarnIcon from "@/shared/assets/icons/warning.svg";

const data: PatientStateInfo = [
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
    <PatientStateCard
      icon={WarnIcon}
      link={getRouteDigitalProfile()}
      title="Оценка рисков"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
