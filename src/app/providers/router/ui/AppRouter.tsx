import { memo, Suspense } from "react";
import { Route, type RouteProps, Routes } from "react-router-dom";

import { routeConfig } from "../config/routeConfig";

const renderWithWrapper = (route: RouteProps) => {
  const element = <Suspense fallback="Loading...">{route.element}</Suspense>;

  return <Route key={route.path} path={route.path} element={element} />;
};

const AppRouter = () => (
  <Routes>{Object.values(routeConfig).map(renderWithWrapper)}</Routes>
);

export default memo(AppRouter);
