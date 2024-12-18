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
        <h2>Recommendations</h2>
        <TextField
          className={cls.input}
          label="Treatment plan"
          variant="outlined"
          value={plan}
          rows={4}
          onChange={(e) => setPlan(e.target.value)}
          multiline
        />
        <TextField
          className={cls.input}
          label="Drugs and dosages"
          variant="outlined"
          value={medicines}
          rows={4}
          onChange={(e) => setMedicines(e.target.value)}
          multiline
        />
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="ru">
          <DatePicker
            className={cls.input}
            label="Date"
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
          Save
        </Button>
      </form>
    </Modal>
  );
};
