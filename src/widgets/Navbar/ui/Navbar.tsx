import { classNames } from "@/shared/lib/classNames";
import cls from "./Navbar.module.scss";
import { memo } from "react";
import { AppLink } from "@/shared/ui/AppLink";
import {
  getRouteDigitalProfile,
  getRouteStatePanel,
} from "@/shared/const/router";

interface NavbarProps {
  className?: string;
}

export const Navbar = memo(({ className }: NavbarProps) => {
  return (
    <header className={classNames(cls.Navbar, {}, [className])}>
      <AppLink to={getRouteDigitalProfile()} className={cls.createBtn}>
        Цифровой профиль
      </AppLink>
      <AppLink to={getRouteStatePanel()} className={cls.createBtn}>
        Панель состояния
      </AppLink>
    </header>
  );
});
