import cls from "./GeneralInfo.module.scss";
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
    name: "Возраст",
    value: "30",
  },
  {
    name: "Пол",
    value: "Мужской",
  },
  {
    name: "Дата рождения",
    value: "27.07.1994",
  },
  {
    name: "Рост",
    value: "170",
    unit: "см",
    date: "10-20-2024",
  },
  {
    name: "Вес",
    value: "60",
    unit: "кг",
    date: "10-20-2024",
  },
  {
    name: "ИМТ",
    value: "24.2",
    unit: "кг/м^3",
    date: "10-20-2024",
  },
  {
    name: "Температура",
    value: "36",
    unit: "°C",
    date: "10-20-2024",
  },
  {
    name: "Систолическое АД",
    value: "160",
    unit: "мм рт.ст.",
    date: "10-20-2024",
  },
  {
    name: "Диастолическое АД",
    value: "100",
    unit: "мм рт.ст.",
    date: "10-20-2024",
  },
  {
    name: "ЧСС",
    value: "90",
    unit: "уд/мин",
    date: "10-20-2024",
  },
  {
    name: "Частота дыхания",
    value: "30",
    unit: "число/мин",
    date: "10-20-2024",
  },
];
interface GeneralInfoProps {
  className?: string;
}

export const GeneralInfo = (props: GeneralInfoProps) => {
  return (
    <Accordion defaultExpanded>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Общая информация
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
