import cls from "./FamilyInfo.module.scss";
import {
  HealthMeasurement,
  type HealthMeasurementData,
} from "@/entities/HealthMeasurement";
import {
  Accordion,
  AccordionActions,
  AccordionDetails,
  AccordionSummary,
  Button,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";

const data: HealthMeasurementData[] = [
  { name: "Отец", value: "Артериальная гипертензия, с 45 лет" },
  { name: "Мать", value: "Ишемическая болезнь сердца, с 50 лет" },
  { name: "Дед по отцовской линии", value: "Инфаркт миокарда, в 60 лет" },
  {
    name: "Бабушка по материнской линии",
    value: "Сахарный диабет 2 типа, с 55 лет",
  },
];

interface FamilyInfoProps {
  className?: string;
}

export const FamilyInfo = (props: FamilyInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Family history
      </AccordionSummary>
      <AccordionDetails className={cls.content}>
        {data.map((measurement) => (
          <HealthMeasurement data={measurement} key={measurement.name} />
        ))}
      </AccordionDetails>
      <AccordionActions>
        <Button>Редактировать</Button>
      </AccordionActions>
    </Accordion>
  );
};
