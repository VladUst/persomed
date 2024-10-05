import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStateInfoList.module.scss";
import type {
  PatientStateItem,
  PatientStateInfo,
} from "../../model/types/patientStateInfo";
import { memo } from "react";

interface PatientStateInfoListProps {
  className?: string;
  data: PatientStateInfo;
}

const PatientStateInfoListItem = memo((props: PatientStateItem) => {
  const { text, Icon, label } = props;
  return (
    <li className={cls.listItem}>
      {Icon && <span>Icon</span>}
      <p>{text}</p>
      {label && <span>{label}</span>}
    </li>
  );
});

export const PatientStateInfoList = memo((props: PatientStateInfoListProps) => {
  const { className, data } = props;

  return (
    <ul className={classNames(cls.PatientStateInfoList, {}, [className])}>
      {data.map((item) => (
        <PatientStateInfoListItem key={item.text} {...item} />
      ))}
    </ul>
  );
});
