import { useEffect } from "react";
import { useParams } from "react-router-dom";
import { RateDetailsPage } from "./RateDetailsPage/RateDetailsPage";
import { RiskDetailsPage } from "./RiskDetailsPage/RiskDetailsPage";
import cls from "./StatusDetailsPage.module.scss";
import { DiseasesDetailsPage } from "./DiseasesDetailsPage/DiseasesDetailsPage";
import { SymptomsDetailsPage } from "./SymptomsDetailsPage/SymptomsDetailsPage";
import { SuspicionsDetailsPage } from "./SuspicionsDetailsPage/SuspicionsDetailsPage";
import { MedicinesDetailsPage } from "./MedicinesDetailsPage/MedicinesDetailsPage";
import { RecommendationsDetailsPage } from "./RecommendationsDetailsPage/RecommendationsDetailsPage";

export const StatusDetailsPage = () => {
  const { id } = useParams<{ id: string }>();
  useEffect(() => {
    console.log(id);
  }, [id]);

  if (id === "rates") {
    return <RateDetailsPage />;
  }

  if (id === "risks") {
    return <RiskDetailsPage />;
  }

  if (id === "diseases") {
    return <DiseasesDetailsPage />;
  }

  if (id === "symptoms") {
    return <SymptomsDetailsPage />;
  }

  if (id === "suspicions") {
    return <SuspicionsDetailsPage />;
  }

  if (id === "medicines") {
    return <MedicinesDetailsPage />;
  }

  if (id === "recommendations") {
    return <RecommendationsDetailsPage />;
  }

  return (
    <div className={cls.document}>
      <div className={cls.message}>Ресурс не найден</div>
    </div>
  );
};
