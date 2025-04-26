import { Page } from "@/widgets/Page";
import cls from "./RecommendationsDetailsPage.module.scss";
import { Divider } from "@mui/material";

const recommendations = [
  {
    name: "Омега 3",
    source: "Сервис рекомендаций препаратов",
    dosage: "1000 мг./ден.",
    date: "2024-03-15",
  },
  {
    name: "Альфа-липоевая кислота",
    source: "Сервис рекомендаций препаратов",
    dosage: "600 мг./ден.",
    date: "2024-03-15",
  },
  {
    name: "Магний",
    source: "Сервис рекомендаций препаратов",
    dosage: "400 мг./ден.",
    date: "2024-03-15",
  },
  {
    name: "Ограничить употребление сахара",
    source: "Общие рекомендации по хроническим заболеваниям. Кардиолог",
    date: "2024-03-09",
  },
  {
    name: "Регулярные аэробные нагрузки",
    source: "Общие рекомендации по хроническим заболеваниям. Кардиолог",
    date: "2024-03-09",
  },
];

const renderRecommendations = () =>
  recommendations.map((recommendation, index) => (
    <div key={index}>
      <Divider textAlign="left" className={cls.divider}>
        {recommendation.name}
      </Divider>
      <p>
        <span className={cls.sectionLabel}>Источник:</span>{" "}
        {recommendation.source}
      </p>
      {recommendation.dosage && (
        <p>
          <span className={cls.sectionLabel}>Дозировка:</span>{" "}
          {recommendation.dosage}
        </p>
      )}
      <p>
        <span className={cls.sectionLabel}>Дата назначения:</span>{" "}
        {recommendation.date}
      </p>
    </div>
  ));

export const RecommendationsDetailsPage = () => {
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Рекомендации</h1>
        <section className={cls.content}>{renderRecommendations()}</section>
      </article>
    </Page>
  );
};
