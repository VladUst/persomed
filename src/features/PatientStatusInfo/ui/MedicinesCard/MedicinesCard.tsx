import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import { getRouteDigitalProfile } from "@/shared/const/router";
import MedicinesIcon from "@/shared/assets/icons/medicine.svg";

const data: PatientStatusInfo = [
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
    <PatientStatusCard
      icon={MedicinesIcon}
      link={getRouteDigitalProfile()}
      title="Лекарства"
      className={className}
      variant={PatientStatusCardVariant.GREEN}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
