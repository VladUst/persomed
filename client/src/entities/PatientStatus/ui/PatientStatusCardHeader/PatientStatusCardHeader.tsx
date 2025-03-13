import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStatusCardHeader.module.scss";
import { Icon } from "@/shared/ui/Icon";
import { AppLink } from "@/shared/ui/AppLink";
import { getRouteStatusDetails } from "@/shared/const/router";

interface PatientStatusCardHeaderProps {
  id: string;
  className?: string;
  title: string;
  icon: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
}

export const PatientStatusCardHeader = (
  props: PatientStatusCardHeaderProps,
) => {
  const { className, title, icon, id } = props;
  return (
    <div className={classNames(cls.PatientStatusCardHeader, {}, [className])}>
      <div className={cls.title}>
        <Icon Svg={icon} />
        {title}
      </div>
      <AppLink className={cls.link} to={getRouteStatusDetails(id)}>
        Подробнее
      </AppLink>
    </div>
  );
};
