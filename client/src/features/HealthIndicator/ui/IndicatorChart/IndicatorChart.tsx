import { Button, Modal } from "@mui/material";
import cls from "./IndicatorChart.module.scss";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from "recharts";
import { classNames } from "@/shared/lib/classNames";
import { useState } from "react";
import type { HealthIndicator } from "@/entities/HealthIndicator";
import { getMeasurment } from "@/entities/HealthIndicator";

const data = [
  {
    name: "30.01.24",
    value: 4.7,
  },
  {
    name: "23.03.24",
    value: 5.5,
  },
  {
    name: "08.05.24",
    value: 4.2,
  },
  {
    name: "17.08.24",
    value: 6.3,
  },
  {
    name: "20.10.24",
    value: 7.5,
  },
];

interface IndicatorChartProps {
  className?: string;
  indicatorData: HealthIndicator;
  isOpen: boolean;
  onClose: () => void;
}

export const IndicatorChart = (props: IndicatorChartProps) => {
  const { className, indicatorData, isOpen, onClose } = props;

  const [isLevelsVisible, setIsLevelsVisible] = useState(false);
  const onToggle = () => {
    setIsLevelsVisible((prev) => !prev);
  };

  return (
    <Modal open={isOpen} onClose={onClose}>
      <div className={classNames(cls.IndicatorChart, {}, [className])}>
        <div className={cls.title}>
          <h2>{indicatorData.name}</h2>
          {getMeasurment(
            indicatorData.unit,
            indicatorData.targetLevel,
            indicatorData.value,
          )}
        </div>
        <LineChart
          width={800}
          height={400}
          data={data}
          margin={{
            top: 50,
            right: 20,
            left: 20,
            bottom: 30,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" dy={10} />
          <YAxis />
          <Tooltip formatter={(value: string) => [`${value}`, "Значение"]} />

          {isLevelsVisible && (
            <>
              <ReferenceLine
                y={indicatorData.targetLevel[1]}
                label="Max"
                stroke="red"
              />
              <ReferenceLine
                y={indicatorData.targetLevel[0]}
                label="Min"
                stroke="red"
              />
            </>
          )}

          <Line
            type="linear"
            dataKey="value"
            stroke="var(--primary-color)"
            activeDot={{ r: 8 }}
          />
        </LineChart>
        <Button className={cls.btn} onClick={onToggle}>
          {isLevelsVisible
            ? "Скрыть допустимые диапазоны"
            : "Показать допустимые диапазоны"}
        </Button>
      </div>
    </Modal>
  );
};
