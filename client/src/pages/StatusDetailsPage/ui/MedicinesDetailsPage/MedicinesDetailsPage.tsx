import { Page } from "@/widgets/Page";
import cls from "./MedicinesDetailsPage.module.scss";
import { Divider } from "@mui/material";

const medicines = [
  {
    name: "Лозартан",
    source: "Препараты для лечения гипертензии. Кардиолог",
    dosage: "50 мг./ден.",
    date: "2024-03-05",
  },
  {
    name: "Эналаприл",
    source: "Препараты для лечения гипертензии. Кардиолог",
    dosage: "5 мг./ден.",
    date: "2024-03-05",
  },
  {
    name: "Амлодипин",
    source: "Препараты для лечения гипертензии. Кардиолог",
    dosage: "5 мг./ден.",
    date: "2024-03-05",
  },
];

const renderMedicines = () =>
  medicines.map((medicine, index) => (
    <div key={index}>
      <Divider textAlign="left" className={cls.divider}>
        {medicine.name}
      </Divider>
      <p>
        <span className={cls.sectionLabel}>Источник:</span> {medicine.source}
      </p>
      <p>
        <span className={cls.sectionLabel}>Дозировка:</span> {medicine.dosage}
      </p>
      <p>
        <span className={cls.sectionLabel}>Дата назначения:</span>{" "}
        {medicine.date}
      </p>
    </div>
  ));

export const MedicinesDetailsPage = () => {
  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Лекарства</h1>
        <section className={cls.content}>{renderMedicines()}</section>
      </article>
    </Page>
  );
};
