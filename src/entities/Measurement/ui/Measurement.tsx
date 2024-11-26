import { classNames } from "@/shared/lib/classNames";
import type { HealthMeasurement } from "../model/HealthMeasurement";
import cls from "./HealthIndicatorCard.module.scss";

interface MeasurementProps {
  className?: string;
  data: HealthMeasurement;
}

export const Measurement = (props: MeasurementProps) => {
  const { className, data } = props;

  return (
    <div className={classNames(cls.Measurement, {}, [className])}>
      <h6 className={cls.title}>
        {data.name}
        {data.unit && `, ${data.unit}`}
      </h6>
      <div className={cls.value}>
        <p>{data.value}</p>
        (data.date && <span>{data.date}</span>)
      </div>
    </div>
  );
};
