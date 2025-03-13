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
      <AppLink to={getRouteDigitalProfile()}>Цифровой профиль</AppLink>
      <AppLink to={getRouteHealthIndicators()}>Показатели здоровья</AppLink>
      <AppLink to={getRouteStatusPanel()}>Панель состояния</AppLink>
      <AppLink to={getRouteChat()}>Чат</AppLink>
    </header>
  );
});
