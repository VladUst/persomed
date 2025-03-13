import { lazy } from "react";

export const StatusPanelPageAsync = lazy(() =>
  import("./StatusPanelPage").then((module) => ({
    default: module.StatusPanelPage,
  })),
);
