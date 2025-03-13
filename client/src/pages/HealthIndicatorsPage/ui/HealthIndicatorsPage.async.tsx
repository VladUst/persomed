import { lazy } from "react";

export const HealthIndicatorsPageAsync = lazy(() =>
  import("./HealthIndicatorsPage").then((module) => ({
    default: module.HealthIndicatorsPage,
  })),
);
