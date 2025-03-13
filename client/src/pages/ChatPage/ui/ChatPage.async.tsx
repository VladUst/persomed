import { lazy } from "react";

export const ChatPageAsync = lazy(() =>
  import("./ChatPage").then((module) => ({
    default: module.ChatPage,
  })),
);
