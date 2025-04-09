import {
  Autocomplete,
  Box,
  Button,
  Chip,
  FormControl,
  InputLabel,
  MenuItem,
  Modal,
  Select,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import cls from "./InfoForm.module.scss";
import { classNames } from "@/shared/lib/classNames";
import { useEffect, useState } from "react";
import { nosologyOptions, ontology } from "../../model/ontology";
import type { Nosology } from "../../model/types";

interface AnamnesisFormProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
}

interface FormState {
  patientName: string;
  nosology: Nosology | "";
  generalState: string;
  temperature: string;
  systolicPressure: string;
  diastolicPressure: string;
  heartRate: string;
  symptoms: string[];
}

export const AnamnesisForm = (props: AnamnesisFormProps) => {
  const { className, isOpen, onClose } = props;

  const [formState, setFormState] = useState<FormState>({
    patientName: "",
    nosology: "",
    generalState: "",
    temperature: "",
    systolicPressure: "",
    diastolicPressure: "",
    heartRate: "",
    symptoms: [],
  });

  const [symptomOptions, setSymptomOptions] = useState<string[]>([]);

  useEffect(() => {
    if (formState.nosology) {
      setSymptomOptions(ontology[formState.nosology as Nosology]);
    } else {
      setSymptomOptions([]);
    }
  }, [formState.nosology]);

  const handleChange = <T extends keyof FormState>(
    field: T,
    value: FormState[T],
  ) => {
    setFormState((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would handle form submission
    console.log(formState);
    onClose();
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <form
        className={classNames(cls.InfoForm, {}, [className])}
        onSubmit={handleSubmit}
      >
        <Typography variant="h5" component="h2" gutterBottom>
          Анамнез
        </Typography>

        <TextField
          className={cls.input}
          label="ФИО пациента"
          variant="outlined"
          fullWidth
          value={formState.patientName}
          onChange={(e) => handleChange("patientName", e.target.value)}
          margin="normal"
        />

        <FormControl className={cls.input} fullWidth margin="normal">
          <InputLabel id="nosology-select-label">Класс заболеваний</InputLabel>
          <Select
            labelId="nosology-select-label"
            value={formState.nosology}
            label="Класс заболеваний"
            onChange={(e) =>
              handleChange("nosology", e.target.value as Nosology)
            }
          >
            {nosologyOptions.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          className={cls.input}
          label="Общее состояние"
          variant="outlined"
          fullWidth
          value={formState.generalState}
          rows={4}
          onChange={(e) => handleChange("generalState", e.target.value)}
          multiline
          margin="normal"
        />

        <Autocomplete
          multiple
          freeSolo
          fullWidth
          options={symptomOptions}
          value={formState.symptoms}
          onChange={(_, newValue) => handleChange("symptoms", newValue)}
          renderTags={(value, getTagProps) =>
            value.map((option, index) => (
              // eslint-disable-next-line react/jsx-key
              <Chip
                variant="outlined"
                label={option}
                {...getTagProps({ index })}
              />
            ))
          }
          renderInput={(params) => (
            <TextField
              {...params}
              className={cls.input}
              variant="outlined"
              label="Симптомы"
              placeholder="Добавить симптом"
              fullWidth
              margin="normal"
            />
          )}
          sx={{ width: "100%" }}
        />

        <TextField
          className={cls.input}
          label="Температура тела (°C)"
          variant="outlined"
          fullWidth
          value={formState.temperature}
          onChange={(e) => handleChange("temperature", e.target.value)}
          type="number"
          margin="normal"
        />

        <Stack direction="row" spacing={2} sx={{ width: "100%", mt: 2, mb: 2 }}>
          <TextField
            label="Систолическое давление (мм рт.ст.)"
            variant="outlined"
            fullWidth
            value={formState.systolicPressure}
            onChange={(e) => handleChange("systolicPressure", e.target.value)}
            type="number"
            sx={{ flex: 1 }}
          />
          <TextField
            label="Диастолическое давление (мм рт.ст.)"
            variant="outlined"
            fullWidth
            value={formState.diastolicPressure}
            onChange={(e) => handleChange("diastolicPressure", e.target.value)}
            type="number"
            sx={{ flex: 1 }}
          />
        </Stack>

        <TextField
          className={cls.input}
          label="Пульс (ЧСС, уд/мин)"
          variant="outlined"
          fullWidth
          value={formState.heartRate}
          onChange={(e) => handleChange("heartRate", e.target.value)}
          type="number"
          margin="normal"
        />

        <Box sx={{ mt: 3 }}>
          <Button
            className={cls.btn}
            type="submit"
            variant="contained"
            size="large"
            fullWidth
          >
            Сохранить
          </Button>
        </Box>
      </form>
    </Modal>
  );
};
