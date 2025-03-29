import { classNames } from "@/shared/lib/classNames";
import type { HealthMeasurementData } from "../model/types";
import cls from "./HealthMeasurement.module.scss";
import { IconButton } from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

interface HealthMeasurementProps {
  className?: string;
  data: HealthMeasurementData;
  onEdit?: (data: HealthMeasurementData) => void;
  onDelete?: (id: string) => void;
}

const getValue = (value?: string, date?: string) => {
  if (!value) {
    return <p className={cls.value_non}>-</p>;
  }
  return (
    <div className={cls.value}>
      <p>{value}</p>
      {date && <span>{date}</span>}
    </div>
  );
};

export const HealthMeasurement = (props: HealthMeasurementProps) => {
  const { className, data, onEdit, onDelete } = props;

  const handleEdit = () => {
    if (onEdit) {
      onEdit(data);
    }
  };

  const handleDelete = () => {
    if (onDelete) {
      onDelete(data.id);
    }
  };

  return (
    <div className={classNames(cls.Measurement, {}, [className])}>
      <div className={cls.header}>
        <h5 className={cls.title}>
          {data.name}
          {data.unit && `, ${data.unit}`}
        </h5>
        <div className={cls.actions}>
          <IconButton size="small" onClick={handleEdit}>
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton size="small" onClick={handleDelete}>
            <DeleteIcon fontSize="small" />
          </IconButton>
        </div>
      </div>
      {getValue(data.value, data.date)}
    </div>
  );
};
