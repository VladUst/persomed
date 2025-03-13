import { classNames } from "@/shared/lib/classNames";
import type { HealthIndicator } from "../../model/types/HealthIndicator";
import cls from "./HealthIndicatorCard.module.scss";
import { Icon } from "@/shared/ui/Icon";
import EditIcon from "@/shared/assets/icons/edit.svg";
import ChartIcon from "@/shared/assets/icons/chart.svg";
import { IconButton } from "@mui/material";

interface HealthIndicatorCardProps {
  className?: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  data: HealthIndicator;
  onShowChart?: () => void;
  onShowForm?: () => void;
}

export const getMeasurment = (
  unit: string,
  targetLevel: [number, number],
  value?: string,
) => {
  if (!value) {
    return <p>Нет данных</p>;
  }
  const val = parseInt(value);
  if (val >= targetLevel[0] && val <= targetLevel[1]) {
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
  const { className, icon, data, onShowChart, onShowForm } = props;

  const openChart = () => {
    onShowChart?.();
  };

  const openForm = () => {
    onShowForm?.();
  };

  return (
    <article className={classNames(cls.HealthIndicatorCard, {}, [className])}>
      <div className={cls.header}>
        <div className={cls.title}>
          <Icon className={cls.icon} Svg={icon} />
          <h4>{data.name}</h4>
        </div>
        <div>
          <IconButton onClick={openForm}>
            <EditIcon className={cls.iconBtn} />
          </IconButton>
          <IconButton onClick={openChart}>
            <ChartIcon className={cls.iconBtn} />
          </IconButton>
        </div>
      </div>
      <div className={cls.content}>
        {getMeasurment(data.unit, data.targetLevel, data.value)}
      </div>
      <div className={cls.footer}>
        <div className={cls.date}>
          <span className={cls.label}>Дата обновления</span>
          <span>{data.date ? data.date : "Нет данных"}</span>
        </div>
        <div className={cls.target}>
          <span className={cls.label}>Целевой уровень</span>
          <span>
            {data.targetLevel[0]}-{data.targetLevel[1]}
          </span>
        </div>
      </div>
    </article>
  );
};
