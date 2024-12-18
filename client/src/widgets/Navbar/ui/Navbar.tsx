import { classNames } from "@/shared/lib/classNames";
import cls from "./Navbar.module.scss";
import { memo } from "react";
import { AppLink } from "@/shared/ui/AppLink";
import {
  getRouteChat,
  getRouteDigitalProfile,
  getRouteHealthIndicators,
  getRouteStatusPanel,
} from "@/shared/const/router";

interface NavbarProps {
  className?: string;
}

export const Navbar = memo(({ className }: NavbarProps) => {
  return (
    <header className={classNames(cls.Navbar, {}, [className])}>
      <AppLink to={getRouteDigitalProfile()}>Digital Profile</AppLink>
      <AppLink to={getRouteHealthIndicators()}>Health Indicators</AppLink>
      <AppLink to={getRouteStatusPanel()}>Status Panel</AppLink>
      <AppLink to={getRouteChat()}>Chat</AppLink>
    </header>
  );
});
