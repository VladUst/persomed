import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";
import SearchIcon from "@/shared/assets/icons/search.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStateInfo = [
  {
    text: "Сахарный диабет",
    label: "E10",
  },
];

interface SuspicionsCardProps {
  className?: string;
}

export const SuspicionsCard = (props: SuspicionsCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      icon={SearchIcon}
      link={getRouteDigitalProfile()}
      title="Подозрения"
      className={className}
      variant={PatientStateCardVariant.RED}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
