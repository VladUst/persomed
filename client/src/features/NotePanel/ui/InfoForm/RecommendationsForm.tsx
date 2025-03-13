import { Button, Modal, TextField } from "@mui/material";
import cls from "./InfoForm.module.scss";
import { classNames } from "@/shared/lib/classNames";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import type { Dayjs } from "dayjs";
import { useState } from "react";
import dayjs from "dayjs";

interface RecommendationsFormProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
}

export const RecommendationsForm = (props: RecommendationsFormProps) => {
  const { className, isOpen, onClose } = props;

  const [plan, setPlan] = useState("");
  const [medicines, setMedicines] = useState("");
  const [date, setDate] = useState<Dayjs | null>(dayjs("12-09-2024"));

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form className={classNames(cls.InfoForm, {}, [className])}>
        <h2>Рекомендации</h2>
        <TextField
          className={cls.input}
          label="План лечения"
          variant="outlined"
          value={plan}
          rows={4}
          onChange={(e) => setPlan(e.target.value)}
          multiline
        />
        <TextField
          className={cls.input}
          label="Препараты и дозировки"
          variant="outlined"
          value={medicines}
          rows={4}
          onChange={(e) => setMedicines(e.target.value)}
          multiline
        />
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
          <DatePicker
            className={cls.input}
            label="Дата"
            value={date}
            onChange={(newDate) => setDate(newDate)}
          />
        </LocalizationProvider>

        <Button
          className={cls.btn}
          type="submit"
          variant="contained"
          size="large"
        >
          Сохранить
        </Button>
      </form>
    </Modal>
  );
};
