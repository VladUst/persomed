import {
  PatientStatusCard,
  PatientStatusCardVariant,
} from "@/entities/PatientStatus";
import type { PatientStatusInfo } from "../../model/types/patientStatusInfo";
import { PatientStatusInfoList } from "../PatientStatusInfoList/PatientStatusInfoList";
import FireIcon from "@/shared/assets/icons/fire.svg";

const data: PatientStatusInfo = [
  {
    text: "Высокий шанс сердечного приступа",
  },
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
    text: "Сердечная недостаточность",
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
      id="risks"
      title="Факторы риска"
      className={className}
      variant={PatientStatusCardVariant.RED}
    >
      <PatientStatusInfoList data={data} />
    </PatientStatusCard>
  );
};
