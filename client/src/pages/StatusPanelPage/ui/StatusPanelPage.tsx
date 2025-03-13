import { Page } from "@/widgets/Page";
import cls from "./StatusPanelPage.module.scss";
import {
  DiseasesCard,
  MedicinesCard,
  RateCard,
  RecommendationsCard,
  RisksCard,
  SuspicionsCard,
  SymptomsCard,
} from "@/features/PatientStatusInfo";
export const StatusPanelPage = () => {
  return (
    <Page>
      <section className={cls.wrapperA}>
        <SymptomsCard className={cls.symptoms} />
        <DiseasesCard className={cls.diseases} />
        <RateCard className={cls.rate} />
      </section>
      <section className={cls.wrapperB}>
        <SuspicionsCard className={cls.suspicions} />
        <RisksCard className={cls.risks} />
        <MedicinesCard className={cls.medicines} />
        <RecommendationsCard className={cls.recommendations} />
      </section>
    </Page>
  );
};
