import { lazy } from "react";

export const GeneticProfilePageAsync = lazy(() =>
  import("./GeneticProfilePage").then((module) => ({
    default: module.GeneticProfilePage,
  })),
);
