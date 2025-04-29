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
import { useState } from "react";
import { IndicatorForm } from "@/features/IndicatorForm";

const initialData: HealthMeasurementData[] = [
  {
    id: "1",
    name: "Курение",
    value: "Курит с 20 лет, около 10 сигарет в день",
  },
  {
    id: "2",
    name: "Употребление алкоголя",
    value: "Редкое, 1-2 раза в месяц, умеренные дозы",
  },
  {
    id: "3",
    name: "Физическая активность",
    value: "Минимальная, прогулки 2-3 раза в неделю по 30 минут",
  },
  {
    id: "4",
    name: "Режим сна",
    value: "Нарушен, средняя продолжительность сна 5-6 часов",
  },
  {
    id: "5",
    name: "Питание",
    value:
      "Преобладание жирной пищи, недостаточное количество овощей и фруктов",
  },
];

/* interface LifestyleInfoProps {
  className?: string;
} */

export const LifestyleInfo = () => {
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
          Образ жизни
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
