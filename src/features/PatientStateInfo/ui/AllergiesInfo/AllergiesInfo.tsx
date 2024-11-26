import cls from "./AllergiesInfo.module.scss";
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
  { name: "Антибиотики (пенициллины)", value: "Крапивница и кожный зуд" },
  {
    name: "Нестероидные противовоспалительные средства (ибупрофен)",
    value: "Отек и затрудненное дыхание",
  },
  {
    name: "Ингаляционные аллергены",
    value: "Сезонные аллергии на цветение (пыльца амброзии)",
  },
  {
    name: "Пищевые аллергены",
    value: "Морепродукты: кожный зуд",
  },
];

interface AllergiesInfoProps {
  className?: string;
}

export const AllergiesInfo = (props: AllergiesInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Аллергии и непереносимости
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
