import { lazy } from "react";

export const StatusDetailsPageAsync = lazy(() =>
  import("./StatusDetailsPage").then((module) => ({
    default: module.StatusDetailsPage,
  })),
);
