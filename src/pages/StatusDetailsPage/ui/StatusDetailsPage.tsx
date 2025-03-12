import { Page } from "@/widgets/Page";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import cls from "./StatusDetailsPage.module.scss";
import { Button, Divider } from "@mui/material";
import { RateForm } from "@/features/PatientStatusInfo";

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

  const [isRateFormOpen, setIsRateFormOpen] = useState(false);

  const showRateForm = () => {
    setIsRateFormOpen(true);
  };

  const closeRateForm = () => {
    setIsRateFormOpen(false);
  };

  if (id === "3") {
    return (
      <Page>
        <article className={cls.document}>
          <h1 className={cls.title}>Оценка рисков</h1>
          <section className={cls.content}>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Сердечно-сосудистые заболевания
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Уровень рисков:</span>{" "}
                Высокий
              </p>
              <p>
                <span className={cls.sectionLabel}>Источник:</span> Модель
                оценки рисков сердечно-сосудистых заболеваний
              </p>
              <p>
                <span className={cls.sectionLabel}>Дата оценки:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Ручная оценка
              </Button>
              <RateForm
                isOpen={isRateFormOpen}
                onClose={closeRateForm}
                title="Сердечно-сосудистые заболевания"
                defaultValue={75}
              />
            </div>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Заболевания системы пищеварения
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Уровень рисков:</span>{" "}
                Средний
              </p>
              <p>
                <span className={cls.sectionLabel}>Источник:</span> Ручная
                оценка. Обоснование: Стабильно высокий уровень дисфункций
                желчного пузыря, сопровождаемый...
              </p>
              <p>
                <span className={cls.sectionLabel}>Дата оценки:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Ручная оценка
              </Button>
            </div>
            <div>
              <Divider textAlign="left" className={cls.divider}>
                Заболевания органов дыхания
              </Divider>
              <p>
                <span className={cls.sectionLabel}>Уровень рисков:</span> Низкий
              </p>
              <p>
                <span className={cls.sectionLabel}>Источник:</span> Ручная
                оценка. Обоснование: ...
              </p>
              <p>
                <span className={cls.sectionLabel}>Дата оценки:</span>{" "}
                2024-11-15
              </p>
              <Button
                className={cls.btn}
                onClick={showRateForm}
                variant="outlined"
                size="large"
              >
                Ручная оценка
              </Button>
            </div>
          </section>
        </article>
      </Page>
    );
  }

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
