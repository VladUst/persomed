import { classNames } from "@/shared/lib/classNames";
import type { HealthMeasurementData } from "../model/types";
import cls from "./HealthMeasurement.module.scss";

interface HealthMeasurementProps {
  className?: string;
  data: HealthMeasurementData;
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
  const { className, data } = props;

  return (
    <div className={classNames(cls.Measurement, {}, [className])}>
      <h5 className={cls.title}>
        {data.name}
        {data.unit && `, ${data.unit}`}
      </h5>
      {getValue(data.value, data.date)}
    </div>
  );
};
