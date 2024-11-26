import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStatusCardHeader.module.scss";
import { Icon } from "@/shared/ui/Icon";
import { AppLink } from "@/shared/ui/AppLink";

interface PatientStatusCardHeaderProps {
  className?: string;
  title: string;
  link: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
}

export const PatientStatusCardHeader = (
  props: PatientStatusCardHeaderProps,
) => {
  const { className, title, icon, link } = props;
  return (
    <div className={classNames(cls.PatientStatusCardHeader, {}, [className])}>
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
