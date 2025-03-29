import cls from "./LifestyleInfo.module.scss";
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
  {
    id: "1",
    name: "Курение",
    value: "Курит с 20 лет, около 10 сигарет в день",
  },
  {
    id: "2",
    name: "Употребление алкоголя",
    value: "Редкое, 1-2 раза в месяц, умеренные дозы",
  },
  {
    id: "3",
    name: "Физическая активность",
    value: "Минимальная, прогулки 2-3 раза в неделю по 30 минут",
  },
  {
    id: "4",
    name: "Режим сна",
    value: "Нарушен, средняя продолжительность сна 5-6 часов",
  },
  {
    id: "5",
    name: "Питание",
    value:
      "Преобладание жирной пищи, недостаточное количество овощей и фруктов",
  },
];

interface LifestyleInfoProps {
  className?: string;
}

export const LifestyleInfo = (props: LifestyleInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Образ жизни
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
