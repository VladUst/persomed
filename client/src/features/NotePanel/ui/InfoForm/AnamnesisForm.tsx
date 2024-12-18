import { Button, Modal, TextField } from "@mui/material";
import cls from "./InfoForm.module.scss";
import { classNames } from "@/shared/lib/classNames";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import type { Dayjs } from "dayjs";
import { useState } from "react";
import dayjs from "dayjs";

interface AnamnesisFormProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
}

export const AnamnesisForm = (props: AnamnesisFormProps) => {
  const { className, isOpen, onClose } = props;

  const [state, setState] = useState("");
  const [measurements, setMeasurments] = useState("");
  const [date, setDate] = useState<Dayjs | null>(dayjs("12-09-2024"));

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form className={classNames(cls.InfoForm, {}, [className])}>
        <h2>Anamnesis</h2>
        <TextField
          className={cls.input}
          label="General"
          variant="outlined"
          value={state}
          rows={4}
          onChange={(e) => setState(e.target.value)}
          multiline
        />
        <TextField
          className={cls.input}
          label="Measurements"
          variant="outlined"
          value={measurements}
          rows={2}
          onChange={(e) => setMeasurments(e.target.value)}
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
