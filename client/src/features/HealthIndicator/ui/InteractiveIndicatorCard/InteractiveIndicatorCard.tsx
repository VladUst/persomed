import { HealthIndicatorCard } from "@/entities/HealthIndicator";
import { useState } from "react";
import { IndicatorChart } from "../IndicatorChart/IndicatorChart";
import { IndicatorForm } from "../../../IndicatorForm/IndicatorForm";
import { type HealthMeasurementData } from "@/entities/HealthMeasurement";

interface InteractiveIndicatorCardProps {
  className?: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  data: HealthMeasurementData;
}

export const InteractiveIndicatorCard = (
  props: InteractiveIndicatorCardProps,
) => {
  const { className, icon, data } = props;

  const [isChartOpen, setIsChartOpen] = useState(false);
  const [isFormOpen, setIsFormOpen] = useState(false);

  const showChart = () => {
    setIsChartOpen(true);
  };

  const closeChart = () => {
    setIsChartOpen(false);
  };

  const showForm = () => {
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
  };

  return (
    <>
      <IndicatorForm
        indicatorData={data}
        isOpen={isFormOpen}
        onClose={closeForm}
      />
      <IndicatorChart
        indicatorData={data}
        isOpen={isChartOpen}
        onClose={closeChart}
      />
      <HealthIndicatorCard
        className={className}
        icon={icon}
        data={data}
        onShowChart={showChart}
        onShowForm={showForm}
      />
    </>
  );
};
