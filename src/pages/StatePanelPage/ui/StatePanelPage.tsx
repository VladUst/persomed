import { Page } from "@/widgets/Page";
import cls from "./StatePanelPage.module.scss";
import { PatientStateCard } from "@/entities/PatientState";
import { PatientStateCardVariant } from "@/entities/PatientState/ui/PatientStateCard/PatientStateCard";
export const StatePanelPage = () => {
  return (
    <Page>
      <section className={cls.wrapper}>
        <PatientStateCard
          title="Симптомы"
          className={cls.symptoms}
          variant={PatientStateCardVariant.ORANGE}
        >
          Симптомы
        </PatientStateCard>
        <PatientStateCard
          title="Подозрения"
          className={cls.suspicions}
          variant={PatientStateCardVariant.RED}
        >
          Подозрения
        </PatientStateCard>
        <PatientStateCard
          title="Заболевания"
          className={cls.diseases}
          variant={PatientStateCardVariant.ORANGE}
        >
          Заболевания
        </PatientStateCard>
        <PatientStateCard
          title="Лекарства"
          className={cls.medicines}
          variant={PatientStateCardVariant.GREEN}
        >
          Лекарства
        </PatientStateCard>
        <PatientStateCard
          title="Факторы риска"
          className={cls.risks}
          variant={PatientStateCardVariant.RED}
        >
          Факторы риска
        </PatientStateCard>
        <PatientStateCard
          title="Оценка состояния"
          className={cls.rate}
          variant={PatientStateCardVariant.ORANGE}
        >
          Оценка состояния
        </PatientStateCard>
      </section>
    </Page>
  );
};
