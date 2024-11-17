import type { HealthIndicator } from "@/entities/HealthIndicator";

import { HealthIndicatorCard } from "@/entities/HealthIndicator";
import { useState } from "react";
import { IndicatorChart } from "../IndicatorChart/IndicatorChart";

interface InteractiveIndicatorCardProps {
  className?: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  data: HealthIndicator;
}

export const InteractiveIndicatorCard = (
  props: InteractiveIndicatorCardProps,
) => {
  const { className, icon, data } = props;

  const [isChartOpen, setIsChartOpen] = useState(false);

  const onShowChart = () => {
    setIsChartOpen(true);
  };

  const onCloseChart = () => {
    setIsChartOpen(false);
  };

  return (
    <>
      <IndicatorChart
        indicatorData={data}
        isOpen={isChartOpen}
        onClose={onCloseChart}
      />
      <HealthIndicatorCard
        className={className}
        icon={icon}
        data={data}
        onShowChart={onShowChart}
      />
    </>
  );
};
