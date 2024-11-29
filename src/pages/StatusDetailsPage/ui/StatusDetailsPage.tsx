import { Page } from "@/widgets/Page";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import cls from "./StatusDetailsPage.module.scss";
import { Divider } from "@mui/material";

const riskFactors = [
  {
    name: "Высокий шанс сердечного приступа",
    source: "Модель оценки риска сердечного принципа. Точность работы - 95%",
    date: "2024-11-15",
  },
  {
    name: "Целевое АД не достигнуто",
    source: "Оценка динамики показателей здоровья",
    date: "2024-11-18",
  },
  {
    name: "Целевое ЧСС не достигнуто",
    source: "Оценка динамики показателей здоровья",
    date: "2024-11-20",
  },
  {
    name: "Артериальная гипертензия",
    source: "Хроническое заболевание из истории болезней",
    date: "2024-11-12",
  },
  {
    name: "Сердечная недостаточность",
    source: "Хроническое заболевание из истории болезней",
    date: "2024-11-19",
  },
];

export const StatusDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  useEffect(() => {
    console.log(id);
  }, [id]);

  const renderRiskFactors = () =>
    riskFactors.map((factor, index) => (
      <div key={index}>
        <Divider textAlign="left" className={cls.divider}>
          {factor.name}
        </Divider>
        <p>
          <span className={cls.sectionLabel}>Источник:</span> {factor.source}
        </p>
        <p>
          <span className={cls.sectionLabel}>Дата фиксации:</span> {factor.date}
        </p>
      </div>
    ));

  return (
    <Page>
      <article className={cls.document}>
        <h1 className={cls.title}>Факторы риска</h1>
        <section className={cls.content}>{renderRiskFactors()}</section>
      </article>
    </Page>
  );
};
