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
    name: "Age",
    value: "30",
  },
  {
    name: "Gender",
    value: "Male",
  },
  {
    name: "Date of Birth",
    value: "27.07.1994",
  },
  {
    name: "Height",
    value: "170",
    unit: "cm",
    date: "10-20-2024",
  },
  {
    name: "Weight",
    value: "60",
    unit: "kg",
    date: "10-20-2024",
  },
  {
    name: "BMI",
    value: "24.2",
    unit: "kg/m^3",
    date: "10-20-2024",
  },
  {
    name: "Temperature",
    value: "36",
    unit: "°C",
    date: "10-20-2024",
  },
  {
    name: "Systolic BP",
    value: "160",
    unit: "mmHg",
    date: "10-20-2024",
  },
  {
    name: "Diastolic BP",
    value: "100",
    unit: "mmHg",
    date: "10-20-2024",
  },
  {
    name: "Heart Rate",
    value: "90",
    unit: "bpm",
    date: "10-20-2024",
  },
  {
    name: "Respiratory Rate",
    value: "30",
    unit: "breaths/min",
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
        General information
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
