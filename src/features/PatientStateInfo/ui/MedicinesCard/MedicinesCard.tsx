import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Ибупрофен",
    label: "1 доз./ден.",
  },
  {
    text: "Магний",
    label: "1 доз./ден.",
  },
  {
    text: "Энтерол",
    label: "1 доз./ден.",
  },
];

interface MedicinesCardProps {
  className?: string;
}

export const MedicinesCard = (props: MedicinesCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Лекарства"
      className={className}
      variant={PatientStateCardVariant.GREEN}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
