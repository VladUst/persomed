import { classNames } from "@/shared/lib/classNames";
import { type ReactNode } from "react";
import cls from "./PatientStateCard.module.scss";
import { PatientStateCardHeader } from "../PatientStateCardHeader/PatientStateCardHeader";

export enum PatientStateCardVariant {
  GREEN = "green",
  ORANGE = "orange",
  RED = "red",
}

interface PatientStateCardProps {
  className?: string;
  variant?: PatientStateCardVariant;
  title: string;
  children: ReactNode;
}

export const PatientStateCard = (props: PatientStateCardProps) => {
  const {
    children,
    className,
    title,
    variant = PatientStateCardVariant.GREEN,
  } = props;
  return (
    <article className={classNames(cls.PatientStateCard, {}, [className])}>
      <PatientStateCardHeader title={title} className={cls[variant]} />
      <div className={cls.content}>{children}</div>
    </article>
  );
};
