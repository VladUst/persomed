import { Page } from "@/widgets/Page";
import cls from "./HealthIndicatorsPage.module.scss";
import type { HealthIndicator } from "@/entities/HealthIndicator";
import HeartPulseIcon from "@/shared/assets/icons/heart-pulse.svg";
import {
  AddIndicatorCard,
  InteractiveIndicatorCard,
} from "@/features/HealthIndicator";

const healthIndicators: HealthIndicator[] = [
  {
    id: "1",
    name: "Cholesterol",
    targetLevel: [3.6, 5.2],
    unit: "mmol/L",
  },
  {
    id: "2",
    name: "Body Mass Index",
    value: "24.2",
    targetLevel: [18.5, 24.9],
    date: "10-20-2024",
    unit: "kg/m2",
    targetReached: true,
  },
  {
    id: "3",
    name: "Blood Pressure",
    value: "160/100",
    targetLevel: [120, 80],
    date: "10-20-2024",
    unit: "mmHg",
    targetReached: false,
  },
  {
    id: "4",
    name: "Heart Rate",
    value: "90",
    targetLevel: [60, 80],
    date: "10-20-2024",
    unit: "bpm",
    targetReached: false,
  },
  {
    id: "5",
    name: "Glucose",
    value: "7.5",
    targetLevel: [3.9, 5.6],
    date: "10-20-2024",
    unit: "mmol/L",
    targetReached: false,
  },
  {
    id: "6",
    name: "Potassium",
    value: "3.0",
    targetLevel: [3.5, 5.1],
    date: "10-20-2024",
    unit: "mmol/L",
    targetReached: false,
  },
  {
    id: "7",
    name: "Vitamin D",
    value: "38",
    targetLevel: [20, 50],
    date: "10-20-2024",
    unit: "ng/mL",
    targetReached: true,
  },
  {
    id: "8",
    name: "SpO2",
    value: "98",
    targetLevel: [95, 100],
    date: "10-20-2024",
    unit: "%",
    targetReached: true,
  },
];

export const HealthIndicatorsPage = () => {
  return (
    <Page>
      <section className={cls.wrapper}>
        {healthIndicators.map((data) => {
          return (
            <InteractiveIndicatorCard
              key={data.id}
              data={data}
              icon={HeartPulseIcon}
            />
          );
        })}
        <AddIndicatorCard />
      </section>
    </Page>
  );
};
