import { Page } from "@/widgets/Page";
import cls from "./HealthIndicatorsPage.module.scss";
import HeartPulseIcon from "@/shared/assets/icons/heart-pulse.svg";
import {
  AddIndicatorCard,
  InteractiveIndicatorCard,
} from "@/features/HealthIndicator";
import { type HealthMeasurementData } from "@/entities/HealthMeasurement";

const healthIndicators: HealthMeasurementData[] = [
  {
    id: "1",
    name: "Холестерин",
    targetLevelMin: 3.6,
    targetLevelMax: 5.2,
    unit: "ммоль/л",
  },
  {
    id: "2",
    name: "Индекс массы тела",
    value: "24.2",
    targetLevelMin: 18.5,
    targetLevelMax: 24.9,
    date: "10-20-2024",
    unit: "кг/м3",
    targetReached: true,
  },
  {
    id: "3",
    name: "Артериальное давление",
    value: "160/100",
    targetLevelMin: 120,
    targetLevelMax: 80,
    date: "10-20-2024",
    unit: "мм рт.ст.",
    targetReached: false,
  },
  {
    id: "4",
    name: "Частота сердечных сокращений",
    value: "90",
    targetLevelMin: 60,
    targetLevelMax: 80,
    date: "10-20-2024",
    unit: "уд/мин",
    targetReached: false,
  },
  {
    id: "5",
    name: "Глюкоза",
    value: "7.5",
    targetLevelMin: 3.9,
    targetLevelMax: 5.6,
    date: "10-20-2024",
    unit: "ммоль/л",
    targetReached: false,
  },
  {
    id: "6",
    name: "Калий",
    value: "3.0",
    targetLevelMin: 3.5,
    targetLevelMax: 5.1,
    date: "10-20-2024",
    unit: "ммоль/л",
    targetReached: false,
  },
  {
    id: "7",
    name: "Витамин D",
    value: "38",
    targetLevelMin: 20,
    targetLevelMax: 50,
    date: "10-20-2024",
    unit: "нг/мл",
    targetReached: true,
  },
  {
    id: "8",
    name: "SpO2",
    value: "98",
    targetLevelMin: 95,
    targetLevelMax: 100,
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
