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
import { useState } from "react";
import { IndicatorForm } from "@/features/IndicatorForm";

const initialData: HealthMeasurementData[] = [
  {
    id: "1",
    name: "Отец",
    value: "Артериальная гипертензия, с 45 лет",
  },
  {
    id: "2",
    name: "Мать",
    value: "Ишемическая болезнь сердца, с 50 лет",
  },
  {
    id: "3",
    name: "Бабушка по материнской линии",
    value: "Сахарный диабет 2 типа, с 55 лет",
  },
];

interface FamilyInfoProps {
  className?: string;
}

export const FamilyInfo = (props: FamilyInfoProps) => {
  const [data, setData] = useState<HealthMeasurementData[]>(initialData);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedIndicator, setSelectedIndicator] = useState<
    HealthMeasurementData | undefined
  >(undefined);

  const handleOpenForm = () => {
    setSelectedIndicator(undefined);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setSelectedIndicator(undefined);
  };

  const handleEdit = (indicator: HealthMeasurementData) => {
    setSelectedIndicator(indicator);
    setIsFormOpen(true);
  };

  const handleDelete = (id: string) => {
    setData(data.filter((item) => item.id !== id));
  };

  const handleSave = (indicator: HealthMeasurementData) => {
    if (selectedIndicator) {
      // Update existing indicator
      setData(
        data.map((item) => (item.id === indicator.id ? indicator : item)),
      );
    } else {
      // Add new indicator
      setData([...data, { ...indicator, id: String(Date.now()) }]);
    }
    handleCloseForm();
  };

  return (
    <>
      <Accordion>
        <AccordionSummary className={cls.title} expandIcon={<ExpandMoreIcon />}>
          Семейный анамез
        </AccordionSummary>
        <AccordionDetails className={cls.content}>
          {data.map((measurement) => (
            <HealthMeasurement
              data={measurement}
              key={measurement.id}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          ))}
        </AccordionDetails>
        <AccordionActions>
          <Button onClick={handleOpenForm}>Добавить</Button>
        </AccordionActions>
      </Accordion>

      <IndicatorForm
        isOpen={isFormOpen}
        onClose={handleCloseForm}
        indicatorData={selectedIndicator}
        onSave={handleSave}
      />
    </>
  );
};
