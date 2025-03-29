import { Page } from "@/widgets/Page";
import { useState } from "react";
import cls from "./RateDetailsPage.module.scss";
import { Button, Divider } from "@mui/material";
import { RateForm } from "@/features/PatientStatusInfo";

export const RateDetailsPage = () => {
  const [isRateFormOpen, setIsRateFormOpen] = useState(false);

  const showRateForm = () => {
    setIsRateFormOpen(true);
  };

  const closeRateForm = () => {
    setIsRateFormOpen(false);
  };

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
              <span className={cls.sectionLabel}>Уровень рисков:</span> Высокий
            </p>
            <p>
              <span className={cls.sectionLabel}>Источник:</span> Модель оценки
              рисков сердечно-сосудистых заболеваний
            </p>
            <p>
              <span className={cls.sectionLabel}>Дата оценки:</span> 2024-11-15
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
              <span className={cls.sectionLabel}>Уровень рисков:</span> Средний
            </p>
            <p>
              <span className={cls.sectionLabel}>Источник:</span> Ручная оценка.
              Обоснование: Стабильно высокий уровень дисфункций желчного пузыря,
              сопровождаемый...
            </p>
            <p>
              <span className={cls.sectionLabel}>Дата оценки:</span> 2024-11-15
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
              <span className={cls.sectionLabel}>Источник:</span> Ручная оценка.
              Обоснование: ...
            </p>
            <p>
              <span className={cls.sectionLabel}>Дата оценки:</span> 2024-11-15
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
};
