import { type RouteProps } from "react-router-dom";
import { DigitalProfilePage } from "@/pages/DigitalProfilePage";
import { StatePanelPage } from "@/pages/StatePanelPage";
import { HealthIndicatorsPage } from "@/pages/HealthIndicatorsPage";
import { ChatPage } from "@/pages/ChatPage";
import {
  AppRoutes,
  getRouteChat,
  getRouteDigitalProfile,
  getRouteHealthIndicators,
  getRouteStatePanel,
} from "@/shared/const/router";

export const routeConfig: Record<AppRoutes, RouteProps> = {
  [AppRoutes.DIGITAL_PROFILE]: {
    path: getRouteDigitalProfile(),
    element: <DigitalProfilePage />,
  },
  [AppRoutes.HEALTH_INDICATORS]: {
    path: getRouteHealthIndicators(),
    element: <HealthIndicatorsPage />,
  },
  [AppRoutes.STATE_PANEL]: {
    path: getRouteStatePanel(),
    element: <StatePanelPage />,
  },
  [AppRoutes.CHAT]: {
    path: getRouteChat(),
    element: <ChatPage />,
  },
  [AppRoutes.NOT_FOUND]: {
    path: "*",
    element: <DigitalProfilePage />,
  },
};
