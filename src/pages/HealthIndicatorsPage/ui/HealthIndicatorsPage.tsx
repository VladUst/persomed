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
    name: "Холестерин",
    targetLevel: [3.6, 5.2],
    unit: "ммоль/л",
  },
  {
    id: "2",
    name: "Индекс массы тела",
    value: "24.2",
    targetLevel: [18.5, 24.9],
    date: "10-20-2024",
    unit: "кг/м3",
    targetReached: true,
  },
  {
    id: "3",
    name: "Артериальное давление",
    value: "160/100",
    targetLevel: [120, 80],
    date: "10-20-2024",
    unit: "мм рт.ст.",
    targetReached: false,
  },
  {
    id: "4",
    name: "Частота сердечных сокращений",
    value: "90",
    targetLevel: [60, 80],
    date: "10-20-2024",
    unit: "уд/мин",
    targetReached: false,
  },
  {
    id: "5",
    name: "Глюкоза",
    value: "7.5",
    targetLevel: [3.9, 5.6],
    date: "10-20-2024",
    unit: "ммоль/л",
    targetReached: false,
  },
  {
    id: "6",
    name: "Калий",
    value: "3.0",
    targetLevel: [3.5, 5.1],
    date: "10-20-2024",
    unit: "ммоль/л",
    targetReached: false,
  },
  {
    id: "7",
    name: "Витамин D",
    value: "38",
    targetLevel: [20, 50],
    date: "10-20-2024",
    unit: "нг/мл",
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
