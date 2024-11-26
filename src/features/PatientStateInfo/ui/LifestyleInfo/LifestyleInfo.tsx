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
  { name: "Курение", value: "Курит с 20 лет, около 10 сигарет в день" },
  {
    name: "Употребление алкоголя",
    value: "Редкое, 1-2 раза в месяц, умеренные дозы",
  },
  {
    name: "Физическая активность",
    value: "Минимальная, прогулки 2-3 раза в неделю по 30 минут",
  },
  {
    name: "Режим сна",
    value: "Нарушен, средняя продолжительность сна 5-6 часов",
  },
  {
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
        Лабораторные и инструментальные измерения
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
