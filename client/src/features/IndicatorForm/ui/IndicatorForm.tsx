import {
  Button,
  Divider,
  Modal,
  TextField,
  Tooltip,
  IconButton,
} from "@mui/material";
import cls from "./IndicatorForm.module.scss";
import { classNames } from "@/shared/lib/classNames";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import type { Dayjs } from "dayjs";
import { useState, useEffect } from "react";
import dayjs from "dayjs";
import { type HealthMeasurementData } from "@/entities/HealthMeasurement";
import HelpOutlineIcon from "@mui/icons-material/HelpOutline";

interface IndicatorFormProps {
  className?: string;
  indicatorData?: HealthMeasurementData;
  isOpen: boolean;
  onClose: () => void;
  onSave?: (data: HealthMeasurementData) => void;
}

export const IndicatorForm = (props: IndicatorFormProps) => {
  const { className, indicatorData, isOpen, onClose, onSave } = props;

  const [name, setName] = useState(indicatorData?.name ?? "");
  const [canonicalName, setCanonicalName] = useState(
    indicatorData?.canonicalName ?? "",
  );
  const [value, setValue] = useState(indicatorData?.value ?? "");
  const [unit, setUnit] = useState(indicatorData?.unit ?? "");
  const [date, setDate] = useState<Dayjs | null>(
    indicatorData?.date ? dayjs(indicatorData.date) : dayjs(),
  );
  const [minTargetLevel, setMinTargetLevel] = useState<number>(
    indicatorData?.targetLevelMin ? indicatorData.targetLevelMin : 0,
  );
  const [maxTargetLevel, setMaxTargetLevel] = useState(
    indicatorData?.targetLevelMax ? indicatorData.targetLevelMax : 0,
  );

  useEffect(() => {
    if (indicatorData) {
      setName(indicatorData.name ?? "");
      setCanonicalName(indicatorData.canonicalName ?? "");
      setValue(indicatorData.value ?? "");
      setUnit(indicatorData.unit ?? "");
      setDate(indicatorData.date ? dayjs(indicatorData.date) : dayjs());
      setMinTargetLevel(indicatorData.targetLevelMin ?? 0);
      setMaxTargetLevel(indicatorData.targetLevelMax ?? 0);
    } else {
      // Reset form when creating a new indicator
      setName("");
      setCanonicalName("");
      setValue("");
      setUnit("");
      setDate(dayjs());
      setMinTargetLevel(0);
      setMaxTargetLevel(0);
    }
  }, [indicatorData, isOpen]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (onSave) {
      const formattedDate = date ? date.format("MM-DD-YYYY") : "";
      const updatedData: HealthMeasurementData = {
        id: indicatorData?.id ?? "",
        canonicalName,
        name: name ?? "",
        value,
        unit,
        date: formattedDate,
        targetLevelMin: minTargetLevel || undefined,
        targetLevelMax: maxTargetLevel || undefined,
      };

      onSave(updatedData);
    }

    onClose();
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form
        className={classNames(cls.IndicatorForm, {}, [className])}
        onSubmit={handleSubmit}
      >
        <h2>{indicatorData ? "Обновить данные" : "Добавить показатель"}</h2>
        <TextField
          className={cls.input}
          label="Название"
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />

        <div className={cls.inputWithTooltip}>
          <TextField
            className={cls.input}
            label="Каноническое название"
            variant="outlined"
            value={canonicalName}
            onChange={(e) => setCanonicalName(e.target.value)}
          />
          <Tooltip title="Необходимо для использования в моделях машинного обучения. Должно быть строго на английском с разделителем между словами в виде нижнего подчеркивания. Пример: 'canonical_name'">
            <IconButton size="small">
              <HelpOutlineIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </div>

        <TextField
          className={cls.input}
          label="Значение"
          variant="outlined"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          multiline
        />

        <TextField
          className={cls.input}
          label="Единица измерения"
          variant="outlined"
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
        />

        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
          <DatePicker
            className={cls.input}
            label="Дата измерения"
            value={date}
            onChange={(newDate) => setDate(newDate)}
          />
        </LocalizationProvider>

        <Divider>Допустимые диапазоны</Divider>

        <div className={cls.horizontalWrapper}>
          <TextField
            label="Минимум"
            variant="outlined"
            type="number"
            value={minTargetLevel}
            onChange={(e) => setMinTargetLevel(parseInt(e.target.value))}
          />
          <TextField
            label="Максимум"
            variant="outlined"
            type="number"
            value={maxTargetLevel}
            onChange={(e) => setMaxTargetLevel(parseInt(e.target.value))}
          />
        </div>
        <Button
          className={cls.btn}
          type="submit"
          variant="contained"
          size="large"
        >
          {indicatorData ? "Обновить" : "Добавить"}
        </Button>
      </form>
    </Modal>
  );
};
