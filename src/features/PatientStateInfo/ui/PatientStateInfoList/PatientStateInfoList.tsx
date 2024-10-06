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
  const { text, Icon, label, labelColor } = props;
  const getLabel = () => {
    if (label) {
      return labelColor ? (
        <span style={{ color: labelColor }} className={cls.label}>
          {label}
        </span>
      ) : (
        <span className={cls.label}>{label}</span>
      );
    }
    return null;
  };

  return (
    <li className={cls.listItem}>
      {Icon && <span>Icon</span>}
      <p>{text}</p>
      {getLabel()}
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
