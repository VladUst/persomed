import cls from "./PreventiveInfio.module.scss";
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
    name: "Противогриппозная вакцина",
    value: "Последняя прививка — октябрь 2023",
  },
  { name: "Прививка от COVID-19", value: "Полный курс, февраль 2021" },
  {
    name: "Вакцинация от гепатита B",
    value: "Привит в детстве, ревакцинация не требовалась",
  },
  {
    name: "Флюорография",
    value: "Последнее обследование — март 2024, без патологий",
  },
  {
    name: "ЭКГ и УЗИ сердца",
    value:
      "Последнее обследование — январь 2024, выявлена сердечная недостаточность",
  },
];

interface PreventiveInfioProps {
  className?: string;
}

export const PreventiveInfio = (props: PreventiveInfioProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Vaccinations and preventive measures
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
