import {
  PatientStateCard,
  PatientStateCardVariant,
} from "@/entities/PatientState";
import type { PatientStateInfo } from "../../model/types/patientStateInfo";
import { PatientStateInfoList } from "../PatientStateInfoList/PatientStateInfoList";

const data: PatientStateInfo = [
  {
    text: "Артериальная гипертензия",
    label: "I10-I15",
  },
  {
    text: "ОРВИ",
    label: "J00-J02",
  },
  {
    text: "Дегенеративно-дистрофическое заболевание позвоночника",
    label: "M40-M54",
  },
];

interface DiseasesCardProps {
  className?: string;
}

export const DiseasesCard = (props: DiseasesCardProps) => {
  const { className } = props;
  return (
    <PatientStateCard
      title="Заболевания"
      className={className}
      variant={PatientStateCardVariant.ORANGE}
    >
      <PatientStateInfoList data={data} />
    </PatientStateCard>
  );
};
