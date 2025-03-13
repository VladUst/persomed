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
    name: "Smoking",
    value: "Smokes since age 20, about 10 cigarettes per day",
  },
  {
    name: "Alcohol Consumption",
    value: "Rare, 1-2 times per month, moderate doses",
  },
  {
    name: "Physical Activity",
    value: "Minimal, walks 2-3 times per week for 30 minutes",
  },
  {
    name: "Sleep Pattern",
    value: "Disturbed, average sleep duration 5-6 hours",
  },
  {
    name: "Diet",
    value: "Predominance of fatty foods, insufficient vegetables and fruits",
  },
];

interface LifestyleInfoProps {
  className?: string;
}

export const LifestyleInfo = (props: LifestyleInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Lifestyle
      </AccordionSummary>
      <AccordionDetails className={cls.content}>
        {data.map((measurement) => (
          <HealthMeasurement data={measurement} key={measurement.name} />
        ))}
      </AccordionDetails>
      <AccordionActions>
        <Button>Edit</Button>
      </AccordionActions>
    </Accordion>
  );
};
