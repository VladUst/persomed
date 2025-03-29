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
    id: "1",
    canonicalName: "age",
    name: "Возраст",
    value: "30",
  },
  {
    id: "2",
    canonicalName: "gender",
    name: "Пол",
    value: "Мужской",
  },
  {
    id: "3",
    canonicalName: "birthdate",
    name: "Дата рождения",
    value: "27.07.1994",
  },
  {
    id: "4",
    canonicalName: "height",
    name: "Рост",
    value: "170",
    unit: "см",
    date: "10-20-2024",
  },
  {
    id: "5",
    canonicalName: "weight",
    name: "Вес",
    value: "60",
    unit: "кг",
    date: "10-20-2024",
  },
  {
    id: "6",
    canonicalName: "BMI",
    name: "ИМТ",
    value: "24.2",
    unit: "кг/м^3",
    date: "10-20-2024",
  },
  {
    id: "7",
    canonicalName: "temperature",
    name: "Температура",
    value: "36",
    unit: "°C",
    date: "10-20-2024",
  },
  {
    id: "8",
    canonicalName: "systolic_pressure",
    name: "Систолическое АД",
    value: "160",
    unit: "мм рт.ст.",
    date: "10-20-2024",
    targetLevelMin: 120,
    targetLevelMax: 140,
  },
  {
    id: "9",
    canonicalName: "diastolic_pressure",
    name: "Диастолическое АД",
    value: "100",
    unit: "мм рт.ст.",
    date: "10-20-2024",
    targetLevelMin: 80,
    targetLevelMax: 90,
  },
  {
    id: "10",
    canonicalName: "heart_rate",
    name: "ЧСС",
    value: "90",
    unit: "уд/мин",
    date: "10-20-2024",
    targetLevelMin: 60,
    targetLevelMax: 80,
  },
  {
    id: "11",
    canonicalName: "respiratory_rate",
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
