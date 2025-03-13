import { lazy } from "react";

export const DigitalProfilePageAsync = lazy(() =>
  import("./DigitalProfilePage").then((module) => ({
    default: module.DigitalProfilePage,
  })),
);
