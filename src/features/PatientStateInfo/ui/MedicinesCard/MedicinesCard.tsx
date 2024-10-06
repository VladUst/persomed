import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import { getRouteDigitalProfile } from "@/shared/const/router";
import MedicinesIcon from "@/shared/assets/icons/medicine.svg";

const data: PatientStateInfo = [
  {
    text: "Лозартан",
    label: "50 мг./ден.",
  },
  {
    text: "Эналаприл",
    label: "5 мг./ден.",
  },
  {
    text: "Амлодипин",
    label: "5 мг./ден.",
  },
];

interface MedicinesCardProps {
  className?: string;
}

export const MedicinesCard = (props: MedicinesCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      icon={MedicinesIcon}
      link={getRouteDigitalProfile()}
      title="Лекарства"
      className={className}
      variant={PatientStateCardVariant.GREEN}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
