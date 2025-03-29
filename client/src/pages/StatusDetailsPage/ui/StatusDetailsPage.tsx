import { useEffect } from "react";
import { useParams } from "react-router-dom";
import { RateDetailsPage } from "./RateDetailsPage/RateDetailsPage";
import { RiskDetailsPage } from "./RiskDetailsPage/RiskDetailsPage";
import cls from "./StatusDetailsPage.module.scss";
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

  return (
    <div className={cls.document}>
      <div className={cls.message}>Ресурс не найден</div>
    </div>
  );
};
