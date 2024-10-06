import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStateCardHeader.module.scss";
import { Icon } from "@/shared/ui/Icon";
import { AppLink } from "@/shared/ui/AppLink";

interface PatientStateCardHeaderProps {
  className?: string;
  title: string;
  link: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
}

export const PatientStateCardHeader = (props: PatientStateCardHeaderProps) => {
  const { className, title, icon, link } = props;
  return (
    <div className={classNames(cls.PatientStateCardHeader, {}, [className])}>
      <div className={cls.title}>
        <Icon Svg={icon} />
        {title}
      </div>
      <AppLink className={cls.link} to={link}>
        Подробнее
      </AppLink>
    </div>
  );
};
