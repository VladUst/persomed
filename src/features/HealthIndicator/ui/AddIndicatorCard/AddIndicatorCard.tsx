import { classNames } from "@/shared/lib/classNames";
import cls from "./AddIndicatorCard.module.scss";
import { Icon } from "@/shared/ui/Icon";
import AddIcon from "@/shared/assets/icons/add.svg";

interface AddIndicatorCardProps {
  className?: string;
}

export const AddIndicatorCard = (props: AddIndicatorCardProps) => {
  const { className } = props;

  return (
    <article className={classNames(cls.AddIndicatorCard, {}, [className])}>
      <div className={cls.wrapper}>
        <Icon className={cls.icon} Svg={AddIcon} />
      </div>

      <h2>Добавить новый показатель...</h2>
    </article>
  );
};
