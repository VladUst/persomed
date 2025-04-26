import { Page } from "@/widgets/Page";
import cls from "./DiseasesDetailsPage.module.scss";
import { Divider } from "@mui/material";

const diseases = [
  {
    name: "ОРВИ",
    source: "История болезней",
    type: "Обычное",
    icd: "J00-J02",
    date: "2024-02-09",
  },
  {
    name: "Артериальная гипертензия",
    source: "История болезней",
    type: "Хроническое",
    icd: "I11",
    date: "2023-01-15",
  },
  {
    name: "Сердечная недостаточность",
    source: "История болезней",
    type: "Хроническое",
    icd: "I50.0",
    date: "2023-02-10",
  },
];

const renderDiseases = () =>
  diseases.map((disease, index) => (
    <div key={index}>
      <Divider textAlign="left" className={cls.divider}>
        {disease.name}
      </Divider>
      <p>
        <span className={cls.sectionLabel}>Источник:</span> {disease.source}
      </p>
      <p>
        <span className={cls.sectionLabel}>Тип:</span> {disease.type}
      </p>
      <p>
        <span className={cls.sectionLabel}>ICD:</span> {disease.icd}
      </p>
      <p>
        <span className={cls.sectionLabel}>Дата фиксации:</span> {disease.date}
      </p>
    </div>
  ));

export const DiseasesDetailsPage = () => {
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Заболевания</h1>
        <section className={cls.content}>{renderDiseases()}</section>
      </article>
    </Page>
  );
};
