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
    name: "Cholesterol",
    unit: "mmol/L",
  },
  {
    name: "Glucose",
    value: "7.5",
    unit: "mmol/L",
    date: "10-20-2024",
  },
  {
    name: "Potassium",
    value: "3.0",
    unit: "mmol/L",
    date: "10-20-2024",
  },
  {
    name: "Vitamin D",
    value: "38",
    unit: "ng/mL",
    date: "10-20-2024",
  },
  {
    name: "Triglycerides",
    unit: "mmol/L",
  },
  {
    name: "Blood Creatinine",
    unit: "mmol/L",
  },
  {
    name: "Glycated Hemoglobin",
    unit: "%",
  },
  {
    name: "24-hour Proteinuria",
    unit: "mg/day",
  },
  {
    name: "Arterial Blood pH",
    unit: "pH",
  },
  {
    name: "Blood Sodium",
    unit: "mmol/L",
  },
  {
    name: "Hematocrit",
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
    unit: "mmHg",
  },
  {
    name: "Atherosclerotic Stenosis of Any Artery",
    unit: "%",
  },
  {
    name: "Left Ventricular Ejection Fraction",
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
        <Button>Edit</Button>
      </AccordionActions>
    </Accordion>
  );
};
