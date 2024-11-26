import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import FireIcon from "@/shared/assets/icons/fire.svg";
import { getRouteDigitalProfile } from "@/shared/const/router";

const data: PatientStatusInfo = [
  {
    text: "Целевое АД не достигнуто",
  },
  {
    text: "Целевое ЧСС не достигнуто",
  },
  {
    text: "Артериальная гипертензия",
  },
  {
    text: "Наличие сердечно-сосудистых заболеваний",
  },
  {
    text: "Увеличение ЧСС в покое",
  },
];

interface RisksCardProps {
  className?: string;
}

export const RisksCard = (props: RisksCardProps) => {
  const { className } = props;
  return (
    <PatientStatusCard
      icon={FireIcon}
      link={getRouteDigitalProfile()}
      title="Факторы риска"
      className={className}
      variant={PatientStatusCardVariant.RED}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
