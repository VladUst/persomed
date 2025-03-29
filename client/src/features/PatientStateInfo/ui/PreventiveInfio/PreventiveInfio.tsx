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
    id: "1",
    name: "Противогриппозная вакцина",
    value: "Последняя прививка — октябрь 2023",
  },
  {
    id: "2",
    name: "Прививка от COVID-19",
    value: "Полный курс, февраль 2021",
  },
  {
    id: "3",
    name: "Вакцинация от гепатита B",
    value: "Привит в детстве, ревакцинация не требовалась",
  },
  {
    id: "4",
    name: "Флюорография",
    value: "Последнее обследование — март 2024, без патологий",
  },
  {
    id: "5",
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
        Вакцинации и профилактические мероприятия
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
