import {
  Autocomplete,
  Box,
  Button,
  FormControl,
  IconButton,
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
import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import {
  diagnosisOptions,
  type Diagnosis,
  medicationsByDiagnosis,
} from "../../model/ontology";

interface RecommendationsFormProps {
  className?: string;
  isOpen: boolean;
  onClose: () => void;
}

interface MedicationItem {
  id: string;
  name: string;
  dosage: string;
  frequency: string;
}

interface FormState {
  patientName: string;
  diagnosis: Diagnosis | "";
  generalRecommendations: string;
  medications: MedicationItem[];
}

export const RecommendationsForm = (props: RecommendationsFormProps) => {
  const { className, isOpen, onClose } = props;

  const [formState, setFormState] = useState<FormState>({
    patientName: "",
    diagnosis: "",
    generalRecommendations: "",
    medications: [{ id: "1", name: "", dosage: "", frequency: "" }],
  });

  const [medicationOptions, setMedicationOptions] = useState<string[]>([]);

  useEffect(() => {
    if (formState.diagnosis) {
      setMedicationOptions(medicationsByDiagnosis[formState.diagnosis]);
    } else {
      setMedicationOptions([]);
    }
  }, [formState.diagnosis]);

  const handleChange = <T extends keyof FormState>(
    field: T,
    value: FormState[T],
  ) => {
    setFormState((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleMedicationChange = (
    id: string,
    field: keyof Omit<MedicationItem, "id">,
    value: string,
  ) => {
    setFormState((prev) => ({
      ...prev,
      medications: prev.medications.map((item) =>
        item.id === id ? { ...item, [field]: value } : item,
      ),
    }));
  };

  const handleAddMedication = () => {
    setFormState((prev) => ({
      ...prev,
      medications: [
        ...prev.medications,
        {
          id: String(Date.now()),
          name: "",
          dosage: "",
          frequency: "",
        },
      ],
    }));
  };

  const handleRemoveMedication = (id: string) => {
    setFormState((prev) => ({
      ...prev,
      medications: prev.medications.filter((item) => item.id !== id),
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
          Рекомендации
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
          <InputLabel id="diagnosis-select-label">Диагноз</InputLabel>
          <Select
            labelId="diagnosis-select-label"
            value={formState.diagnosis}
            label="Диагноз"
            onChange={(e) =>
              handleChange("diagnosis", e.target.value as Diagnosis)
            }
          >
            {diagnosisOptions.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          className={cls.input}
          label="Общие рекомендации"
          variant="outlined"
          fullWidth
          value={formState.generalRecommendations}
          rows={4}
          onChange={(e) =>
            handleChange("generalRecommendations", e.target.value)
          }
          multiline
          margin="normal"
        />

        <Typography variant="subtitle1" gutterBottom sx={{ mt: 1, mb: 1 }}>
          Препараты
        </Typography>

        {formState.medications.map((medication, index) => (
          <Stack
            key={medication.id}
            direction="row"
            spacing={2}
            alignItems="center"
            sx={{ width: "100%", mb: 1 }}
          >
            <Autocomplete
              freeSolo
              options={medicationOptions}
              value={medication.name}
              onChange={(_, newValue) =>
                handleMedicationChange(medication.id, "name", newValue ?? "")
              }
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Название препарата"
                  variant="outlined"
                  fullWidth
                />
              )}
              sx={{ flex: 2 }}
            />
            <TextField
              label="Дозировка"
              variant="outlined"
              fullWidth
              value={medication.dosage}
              onChange={(e) =>
                handleMedicationChange(medication.id, "dosage", e.target.value)
              }
              sx={{ flex: 1 }}
            />
            <TextField
              label="Частота"
              variant="outlined"
              fullWidth
              value={medication.frequency}
              onChange={(e) =>
                handleMedicationChange(
                  medication.id,
                  "frequency",
                  e.target.value,
                )
              }
              sx={{ flex: 1 }}
            />
            {formState.medications.length > 1 && (
              <IconButton
                color="error"
                onClick={() => handleRemoveMedication(medication.id)}
                size="small"
              >
                <DeleteIcon />
              </IconButton>
            )}
          </Stack>
        ))}

        <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
          <IconButton
            color="primary"
            onClick={handleAddMedication}
            size="large"
          >
            <AddIcon />
          </IconButton>
        </Box>

        <Box>
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
