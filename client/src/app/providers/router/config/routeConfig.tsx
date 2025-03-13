import { type RouteProps } from "react-router-dom";
import { DigitalProfilePage } from "@/pages/DigitalProfilePage";
import { HealthIndicatorsPage } from "@/pages/HealthIndicatorsPage";
import { ChatPage } from "@/pages/ChatPage";
import {
  AppRoutes,
  getRouteChat,
  getRouteDigitalProfile,
  getRouteDocumentDetails,
  getRouteHealthIndicators,
  getRouteStatusDetails,
  getRouteStatusPanel,
} from "@/shared/const/router";
import { StatusPanelPage } from "@/pages/StatusPanelPage";
import { DocumentDetailsPage } from "@/pages/DocumentDetailsPage";
import { StatusDetailsPage } from "@/pages/StatusDetailsPage";

export const routeConfig: Record<AppRoutes, RouteProps> = {
  [AppRoutes.DIGITAL_PROFILE]: {
    path: getRouteDigitalProfile(),
    element: <DigitalProfilePage />,
  },
  [AppRoutes.HEALTH_INDICATORS]: {
    path: getRouteHealthIndicators(),
    element: <HealthIndicatorsPage />,
  },
  [AppRoutes.STATUS_PANEL]: {
    path: getRouteStatusPanel(),
    element: <StatusPanelPage />,
  },
  [AppRoutes.CHAT]: {
    path: getRouteChat(),
    element: <ChatPage />,
  },
  [AppRoutes.DOCUMENT_DETAILS]: {
    path: getRouteDocumentDetails(":id"),
    element: <DocumentDetailsPage />,
  },
  [AppRoutes.STATUS_DETAILS]: {
    path: getRouteStatusDetails(":id"),
    element: <StatusDetailsPage />,
  },
  [AppRoutes.NOT_FOUND]: {
    path: "*",
    element: <DigitalProfilePage />,
  },
};
