import { classNames } from "@/shared/lib/classNames";
import { type ReactNode } from "react";
import cls from "./Page.module.scss";

interface PageProps {
  className?: string;
  children: ReactNode;
}

export const Page = (props: PageProps) => {
  const { children } = props;
  return <main className={classNames(cls.Page, {}, [])}>{children}</main>;
};
