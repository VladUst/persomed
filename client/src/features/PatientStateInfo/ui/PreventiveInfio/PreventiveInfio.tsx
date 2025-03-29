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
import { useState } from "react";
import { IndicatorForm } from "@/features/IndicatorForm";

const initialData: HealthMeasurementData[] = [
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
          Вакцинации и профилактические мероприятия
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
