import { Button, Divider, Modal, TextField } from "@mui/material";
import cls from "./IndicatorForm.module.scss";
import { classNames } from "@/shared/lib/classNames";
import type { HealthIndicator } from "@/entities/HealthIndicator";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import type { Dayjs } from "dayjs";
import { useState } from "react";
import dayjs from "dayjs";

interface IndicatorFormProps {
  className?: string;
  indicatorData?: HealthIndicator;
  isOpen: boolean;
  onClose: () => void;
}

export const IndicatorForm = (props: IndicatorFormProps) => {
  const { className, indicatorData, isOpen, onClose } = props;

  const [name, setName] = useState(indicatorData?.name);
  const [value, setValue] = useState(indicatorData?.value);
  const [unit, setUnit] = useState(indicatorData?.unit);
  const [date, setDate] = useState<Dayjs | null>(dayjs(indicatorData?.date));
  const [minTargetLevel, setMinTargetLevel] = useState<number>(
    indicatorData?.targetLevel ? indicatorData.targetLevel[0] : 0,
  );
  const [maxTargetLevel, setMaxTargetLevel] = useState(
    indicatorData?.targetLevel ? indicatorData.targetLevel[1] : 0,
  );

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form className={classNames(cls.IndicatorForm, {}, [className])}>
        <h2>{indicatorData ? "Update data" : "Add indicator"}</h2>
        <TextField
          className={cls.input}
          label="Name"
          variant="outlined"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <TextField
          className={cls.input}
          label="Value"
          variant="outlined"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />

        <TextField
          className={cls.input}
          label="Unit"
          variant="outlined"
          value={unit}
          onChange={(e) => setUnit(e.target.value)}
        />

        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
          <DatePicker
            className={cls.input}
            label="Date"
            value={date}
            onChange={(newDate) => setDate(newDate)}
          />
        </LocalizationProvider>

        <Divider>Acceptable ranges</Divider>

        <div className={cls.horizontalWrapper}>
          <TextField
            label="Min"
            variant="outlined"
            type="number"
            value={minTargetLevel}
            onChange={(e) => setMinTargetLevel(parseInt(e.target.value))}
          />
          <TextField
            label="Max"
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
          {indicatorData ? "Update" : "Add"}
        </Button>
      </form>
    </Modal>
  );
};
