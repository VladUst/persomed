import { type RouteProps } from "react-router-dom";
import { DigitalProfilePage } from "@/pages/DigitalProfilePage";
import { StatePanelPage } from "@/pages/StatePanelPage";
import {
  AppRoutes,
  getRouteDigitalProfile,
  getRouteStatePanel,
} from "@/shared/const/router";

export const routeConfig: Record<AppRoutes, RouteProps> = {
  [AppRoutes.DIGITAL_PROFILE]: {
    path: getRouteDigitalProfile(),
    element: <DigitalProfilePage />,
  },
  [AppRoutes.STATE_PANEL]: {
    path: getRouteStatePanel(),
    element: <StatePanelPage />,
  },
  [AppRoutes.NOT_FOUND]: {
    path: "*",
    element: <DigitalProfilePage />,
  },
};
