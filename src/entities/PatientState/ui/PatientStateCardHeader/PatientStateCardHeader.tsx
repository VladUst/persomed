import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStateCardHeader.module.scss";

interface PatientStateCardHeaderProps {
  className?: string;
  title: string;
}

export const PatientStateCardHeader = (props: PatientStateCardHeaderProps) => {
  const { className, title } = props;
  return (
    <div className={classNames(cls.PatientStateCardHeader, {}, [className])}>
      {title}
    </div>
  );
};
