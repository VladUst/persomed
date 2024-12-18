import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import MedicinesIcon from "@/shared/assets/icons/medicine.svg";

const data: PatientStatusInfo = [
  {
    text: "Losartan",
    label: "50 mg/day",
  },
  {
    text: "Enalapril",
    label: "5 mg/day",
  },
  {
    text: "Amlodipine",
    label: "5 mg/day",
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
      id="6"
      title="Medicines"
      className={className}
      variant={PatientStatusCardVariant.GREEN}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
