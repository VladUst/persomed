import { type LinkProps } from "react-router-dom";
import cls from "./AppLink.module.scss";
import { type ReactNode } from "react";
import { Link } from "react-router-dom";
import { classNames } from "@/shared/lib/classNames";

export enum AppLinkTheme {
  PRIMARY = "primary",
  INVERTED = "inverted",
  RED = "red",
}

interface AppLinkProps extends LinkProps {
  className?: string;
  theme?: AppLinkTheme;
  children: ReactNode;
}

export const AppLink = (props: AppLinkProps) => {
  const {
    to,
    className,
    children,
    theme = AppLinkTheme.PRIMARY,
    ...otherProps
  } = props;
  return (
    <Link
      to={to}
      className={classNames(cls.AppLink, {}, [className, cls[theme]])}
      {...otherProps}
    >
      {children}
    </Link>
  );
};
