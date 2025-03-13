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
  { name: "Antibiotics (Penicillins)", value: "Hives and skin itching" },
  {
    name: "Non-steroidal Anti-inflammatory Drugs (Ibuprofen)",
    value: "Swelling and difficulty breathing",
  },
  {
    name: "Inhalation Allergens",
    value: "Seasonal allergies to flowering (ragweed pollen)",
  },
  {
    name: "Food Allergens",
    value: "Seafood: skin itching",
  },
];

interface AllergiesInfoProps {
  className?: string;
}

export const AllergiesInfo = (props: AllergiesInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Allergies and intolerances
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
