import { lazy } from "react";

export const StatePanelPageAsync = lazy(() =>
  import("./StatePanelPage").then((module) => ({
    default: module.StatePanelPage,
  })),
);
