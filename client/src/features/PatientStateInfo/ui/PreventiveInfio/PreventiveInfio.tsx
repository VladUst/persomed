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
    name: "Flu Vaccine",
    value: "Last vaccination — October 2023",
  },
  { name: "COVID-19 Vaccine", value: "Full course, February 2021" },
  {
    name: "Hepatitis B Vaccination",
    value: "Vaccinated in childhood, revaccination not required",
  },
  {
    name: "Fluorography",
    value: "Last examination — March 2024, no pathologies",
  },
  {
    name: "ECG and Heart Ultrasound",
    value: "Last examination — January 2024, heart failure detected",
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
        <Button>Edit</Button>
      </AccordionActions>
    </Accordion>
  );
};
