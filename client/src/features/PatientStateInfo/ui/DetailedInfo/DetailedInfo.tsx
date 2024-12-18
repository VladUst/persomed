import cls from "./DetailedInfo.module.scss";
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
    name: "Холестерин",
    unit: "ммоль/л",
  },
  {
    name: "Глюкоза",
    value: "7.5",
    unit: "ммоль/л",
    date: "10-20-2024",
  },
  {
    name: "Калий",
    value: "3.0",
    unit: "ммоль/л",
    date: "10-20-2024",
  },
  {
    name: "Витамин D",
    value: "38",
    unit: "нг/мл",
    date: "10-20-2024",
  },
  {
    name: "Триглицериды",
    unit: "ммоль/л",
  },
  {
    name: "Креатинин крови",
    unit: "ммоль/л",
  },
  {
    name: "Гликированный гемоглобин",
    unit: "%",
  },
  {
    name: "Суточная протеинурия",
    unit: "мг/сут",
  },
  {
    name: "pH артериальной крови",
    unit: "pH",
  },
  {
    name: "Натрий крови",
    unit: "ммоль/л",
  },
  {
    name: "Гематокрит",
    unit: "%",
  },
  {
    name: "SpO2",
    value: "98",
    unit: "%",
    date: "10-20-2024",
  },
  {
    name: "PaO2",
    unit: "мм. рт.ст.",
  },
  {
    name: "Атеросклеротический стеноз любой артерии",
    unit: "%",
  },
  {
    name: "Фракция выброса левого желудочка",
    unit: "%",
  },
];
interface DetailedInfoProps {
  className?: string;
}

export const DetailedInfo = (props: DetailedInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Laboratory tests
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
