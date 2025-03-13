import cls from "./FamilyInfo.module.scss";
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
  { name: "Father", value: "Arterial hypertension, since age 45" },
  { name: "Mother", value: "Coronary heart disease, since age 50" },
  { name: "Paternal Grandfather", value: "Myocardial infarction at age 60" },
  {
    name: "Maternal Grandmother",
    value: "Type 2 diabetes, since age 55",
  },
];

interface FamilyInfoProps {
  className?: string;
}

export const FamilyInfo = (props: FamilyInfoProps) => {
  return (
    <Accordion>
      <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
        Family history
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
