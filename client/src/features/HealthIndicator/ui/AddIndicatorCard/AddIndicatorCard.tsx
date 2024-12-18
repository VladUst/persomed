import { classNames } from "@/shared/lib/classNames";
import cls from "./AddIndicatorCard.module.scss";
import { Icon } from "@/shared/ui/Icon";
import AddIcon from "@/shared/assets/icons/add.svg";
import { IndicatorForm } from "../IndicatorForm/IndicatorForm";
import { useState } from "react";

interface AddIndicatorCardProps {
  className?: string;
}

export const AddIndicatorCard = (props: AddIndicatorCardProps) => {
  const { className } = props;
  const [isFormOpen, setIsFormOpen] = useState(false);

  const showForm = () => {
    setIsFormOpen(true);
  };

  const closeForm = () => {
    setIsFormOpen(false);
  };

  return (
    <>
      <IndicatorForm isOpen={isFormOpen} onClose={closeForm} />
      <article
        role="button"
        onClick={showForm}
        className={classNames(cls.AddIndicatorCard, {}, [className])}
      >
        <div className={cls.wrapper}>
          <Icon className={cls.icon} Svg={AddIcon} />
        </div>

        <h2>Add a new metric...</h2>
      </article>
    </>
  );
};
