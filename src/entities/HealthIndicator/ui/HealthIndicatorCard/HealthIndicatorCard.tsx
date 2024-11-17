import { classNames } from "@/shared/lib/classNames";
import type { HealthIndicator } from "../../model/types/HealthIndicator";
import cls from "./HealthIndicatorCard.module.scss";
import { Icon } from "@/shared/ui/Icon";

interface HealthIndicatorCardProps {
  className?: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  data: HealthIndicator;
}

const getMeasurment = (
  unit: string,
  targetReached?: boolean,
  value?: string,
) => {
  if (!value) {
    return <p>Нет данных</p>;
  }
  if (targetReached) {
    return (
      <p className={cls.success}>
        {value} {unit}
      </p>
    );
  } else {
    return (
      <p className={cls.error}>
        {value} {unit}
      </p>
    );
  }
};

export const HealthIndicatorCard = (props: HealthIndicatorCardProps) => {
  const { className, icon, data } = props;

  return (
    <article className={classNames(cls.HealthIndicatorCard, {}, [className])}>
      <div className={cls.header}>
        <div className={cls.title}>
          <Icon className={cls.icon} Svg={icon} />
          <h4>{data.name}</h4>
        </div>
      </div>
      <div className={cls.content}>
        {getMeasurment(data.unit, data.targetReached, data.value)}
      </div>
      <div className={cls.footer}>
        <div className={cls.date}>
          <span className={cls.label}>Дата обновления</span>
          <span>{data.date ? data.date : "Нет данных"}</span>
        </div>
        <div className={cls.target}>
          <span className={cls.label}>Целевой уровень</span>
          <span>{data.targetLevel}</span>
        </div>
      </div>
    </article>
  );
};
