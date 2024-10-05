import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Сердечно сосудистые заболевания",
    label: "Высокие",
  },
  {
    text: "Заболевания органов дыхания",
    label: "Низкие",
  },
  {
    text: "Заболевания системы пищеварения",
    label: "Средние",
  },
  {
    text: "Заболевания эндокринной системы",
    label: "Низкие",
  },
];

interface RateCardProps {
  className?: string;
}

export const RateCard = (props: RateCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Оценка рисков"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
