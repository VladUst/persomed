import { Page } from "@/widgets/Page";
import cls from "./SuspicionsDetailsPage.module.scss";
import { Divider } from "@mui/material";

const suspicions = [
  {
    name: "Сахарный диабет",
    source: "Сервис диагностики",
    icd: "E10",
    date: "2024-07-17",
  },
];

const renderSuspicions = () =>
  suspicions.map((suspicion, index) => (
    <div key={index}>
      <Divider textAlign="left" className={cls.divider}>
        {suspicion.name}
      </Divider>
      <p>
        <span className={cls.sectionLabel}>Источник:</span> {suspicion.source}
      </p>
      <p>
        <span className={cls.sectionLabel}>ICD:</span> {suspicion.icd}
      </p>
      <p>
        <span className={cls.sectionLabel}>Дата фиксации:</span>{" "}
        {suspicion.date}
      </p>
    </div>
  ));

export const SuspicionsDetailsPage = () => {
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Подозрения на заболевания</h1>
        <section className={cls.content}>{renderSuspicions()}</section>
      </article>
    </Page>
  );
};
