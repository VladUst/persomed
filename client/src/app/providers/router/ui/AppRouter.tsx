import { memo, Suspense } from "react";
import { Route, type RouteProps, Routes } from "react-router-dom";

import { routeConfig } from "../config/routeConfig";
import { PageLoader } from "@/widgets/PageLoader";

const renderWithWrapper = (route: RouteProps) => {
  const element = (
    <Suspense fallback={<PageLoader />}>{route.element}</Suspense>
  );

  return <Route key={route.path} path={route.path} element={element} />;
};

const AppRouter = () => (
  <Routes>{Object.values(routeConfig).map(renderWithWrapper)}</Routes>
);

export default memo(AppRouter);
