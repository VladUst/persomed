export enum AppRoutes {
  DIGITAL_PROFILE = "digital_profile",
  HEALTH_INDICATORS = "health_indicators",
  STATUS_PANEL = "status_panel",
  CHAT = "chat",
  DOCUMENT_DETAILS = "document_details",
  STATUS_DETAILS = "status_details",
  NOT_FOUND = "not_found",
}

export const getRouteDigitalProfile = () => "/profile";
export const getRouteHealthIndicators = () => "/indicators";
export const getRouteStatusPanel = () => "/status";
export const getRouteChat = () => "/chat";
export const getRouteDocumentDetails = (id: string) => `/document/${id}`;
export const getRouteStatusDetails = (id: string) => `/status/${id}`;
