import { lazy } from "react";

export const DocumentDetailsPageAsync = lazy(() =>
  import("./DocumentDetailsPage").then((module) => ({
    default: module.DocumentDetailsPage,
  })),
);
