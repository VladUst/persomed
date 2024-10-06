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
  link: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  children: ReactNode;
}

export const PatientStateCard = (props: PatientStateCardProps) => {
  const {
    children,
    className,
    title,
    link,
    icon,
    variant = PatientStateCardVariant.GREEN,
  } = props;
  return (
    <article className={classNames(cls.PatientStateCard, {}, [className])}>
      <PatientStateCardHeader
        link={link}
        icon={icon}
        title={title}
        className={cls[variant]}
      />
      <div className={cls.content}>{children}</div>
    </article>
  );
};
