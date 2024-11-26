import { classNames } from "@/shared/lib/classNames";
import { type ReactNode } from "react";
import cls from "./PatientStatusCard.module.scss";
import { PatientStatusCardHeader } from "../PatientStatusCardHeader/PatientStatusCardHeader";

export enum PatientStatusCardVariant {
  GREEN = "green",
  ORANGE = "orange",
  RED = "red",
}

interface PatientStatusCardProps {
  className?: string;
  variant?: PatientStatusCardVariant;
  title: string;
  link: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  children: ReactNode;
}

export const PatientStatusCard = (props: PatientStatusCardProps) => {
  const {
    children,
    className,
    title,
    link,
    icon,
    variant = PatientStatusCardVariant.GREEN,
  } = props;
  return (
    <article className={classNames(cls.PatientStatusCard, {}, [className])}>
      <PatientStatusCardHeader
        link={link}
        icon={icon}
        title={title}
        className={cls[variant]}
      />
      <div className={cls.content}>{children}</div>
    </article>
  );
};
