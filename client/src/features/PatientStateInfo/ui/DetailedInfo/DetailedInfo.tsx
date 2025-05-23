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
import { useState } from "react";
import { IndicatorForm } from "@/features/IndicatorForm";

const initialData: HealthMeasurementData[] = [
  {
    id: "1",
    canonicalName: "cholesterol",
    name: "Холестерин",
    unit: "ммоль/л",
    targetLevelMin: 3.6,
    targetLevelMax: 5.2,
  },
  {
    id: "2",
    canonicalName: "glucose",
    name: "Глюкоза",
    value: "7.5",
    unit: "ммоль/л",
    date: "10-20-2024",
    targetLevelMin: 3.9,
    targetLevelMax: 5.6,
  },
  {
    id: "3",
    canonicalName: "potassium",
    name: "Калий",
    value: "3.0",
    unit: "ммоль/л",
    date: "10-20-2024",
    targetLevelMin: 3.5,
    targetLevelMax: 5.1,
  },
  {
    id: "4",
    canonicalName: "vitamin_d",
    name: "Витамин D",
    value: "38",
    unit: "нг/мл",
    date: "10-20-2024",
    targetLevelMin: 20,
    targetLevelMax: 50,
  },
  {
    id: "5",
    canonicalName: "triglycerides",
    name: "Триглицериды",
    unit: "ммоль/л",
  },
  {
    id: "6",
    canonicalName: "creatinine",
    name: "Креатинин крови",
    unit: "ммоль/л",
  },
  {
    id: "7",
    canonicalName: "glycated_hemoglobin",
    name: "Гликированный гемоглобин",
    unit: "%",
  },
  {
    id: "8",
    canonicalName: "proteinuria",
    name: "Суточная протеинурия",
    unit: "мг/сут",
  },
  {
    id: "9",
    canonicalName: "pH",
    name: "pH артериальной крови",
    unit: "pH",
  },
  {
    id: "10",
    canonicalName: "sodium",
    name: "Натрий крови",
    unit: "ммоль/л",
  },
  {
    id: "11",
    canonicalName: "hematocrit",
    name: "Гематокрит",
    unit: "%",
  },
  {
    id: "12",
    canonicalName: "SpO2",
    name: "SpO2",
    value: "98",
    unit: "%",
    date: "10-20-2024",
    targetLevelMin: 95,
    targetLevelMax: 100,
  },
  {
    id: "13",
    canonicalName: "PaO2",
    name: "PaO2",
    unit: "мм. рт.ст.",
  },
  {
    id: "14",
    canonicalName: "atherosclerotic_stenosis",
    name: "Атеросклеротический стеноз любой артерии",
    unit: "%",
  },
  {
    id: "15",
    canonicalName: "left_ventricular_function",
    name: "Фракция выброса левого желудочка",
    unit: "%",
  },
];
/* interface DetailedInfoProps {
  className?: string;
} */

export const DetailedInfo = () => {
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
          Лабораторные исследования
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
