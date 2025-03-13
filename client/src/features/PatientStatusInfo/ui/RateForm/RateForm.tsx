import { Box, Button, Modal, Slider, TextField } from "@mui/material";
import cls from "./RateForm.module.scss";
import { classNames } from "@/shared/lib/classNames";

interface RateFormProps {
  className?: string;
  title: string;
  defaultValue: number;
  isOpen: boolean;
  onClose: () => void;
}

const rateMarks = [
  {
    value: 0,
    label: "Неизвестно",
  },
  {
    value: 25,
    label: "Низкий",
  },
  {
    value: 50,
    label: "Средний",
  },
  {
    value: 75,
    label: "Высокий",
  },
  {
    value: 100,
    label: "Критический",
  },
];

function valueToText(value: number) {
  const rate = rateMarks.find((rate) => rate.value === value);
  return rate ? rate.label : "Неизвестно";
}

export const RateForm = (props: RateFormProps) => {
  const { className, title, defaultValue, isOpen, onClose } = props;

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form className={classNames(cls.RateForm, {}, [className])}>
        <h2>{title}</h2>
        <Box sx={{ width: 500 }}>
          <Slider
            defaultValue={defaultValue}
            getAriaValueText={valueToText}
            step={25}
            valueLabelDisplay="auto"
            marks={rateMarks}
          />
        </Box>
        <TextField
          className={cls.input}
          label="Обоснование"
          variant="outlined"
          rows={2}
          multiline
        />
        <Button type="submit" variant="contained" size="large">
          Сохранить
        </Button>
      </form>
    </Modal>
  );
};
