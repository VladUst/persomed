import { Page } from "@/widgets/Page";
import cls from "./SymptomsDetailsPage.module.scss";
import { Divider } from "@mui/material";

const symptoms = [
  {
    name: "Сильная жажда",
    source: "Автоматически извлеченный из анамнеза",
    date: "2024-07-17",
  },
  {
    name: "Полифагия",
    source: "Автоматически извлеченный из анамнеза",
    date: "2024-07-17",
  },
  {
    name: "Потеря веса",
    source: "Автоматически извлеченный из анамнеза",
    date: "2024-07-17",
  },
  {
    name: "Слабость",
    source: "Автоматически извлеченный из анамнеза",
    date: "2024-07-17",
  },
];

const renderSymptoms = () =>
  symptoms.map((symptom, index) => (
    <div key={index}>
      <Divider textAlign="left" className={cls.divider}>
        {symptom.name}
      </Divider>
      <p>
        <span className={cls.sectionLabel}>Источник:</span> {symptom.source}
      </p>
      <p>
        <span className={cls.sectionLabel}>Дата фиксации:</span> {symptom.date}
      </p>
    </div>
  ));

export const SymptomsDetailsPage = () => {
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Симптомы</h1>
        <section className={cls.content}>{renderSymptoms()}</section>
      </article>
    </Page>
  );
};
