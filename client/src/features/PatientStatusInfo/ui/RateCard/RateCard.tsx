import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import WarnIcon from "@/shared/assets/icons/warning.svg";

const data: PatientStatusInfo = [
  {
    text: "Cardiovascular diseases",
    label: "High",
    labelColor: "#E90711",
  },
  {
    text: "Digestive system diseases",
    label: "Moderate",
    labelColor: "#ECB404",
  },
  {
    text: "Respiratory system diseases",
    label: "Low",
    labelColor: "#53D006",
  },
  {
    text: "Endocrine system diseases",
    label: "Low",
    labelColor: "#53D006",
  },
  {
    text: "Kidney and urinary system diseases",
    label: "Low",
    labelColor: "#53D006",
  },
  {
    text: "Musculoskeletal system diseases",
    label: "Unknown",
  },
  {
    text: "Skin and hair diseases",
    label: "Unknown",
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
      id="3"
      title="Risk assessment"
      className={className}
      variant={PatientStatusCardVariant.ORANGE}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
