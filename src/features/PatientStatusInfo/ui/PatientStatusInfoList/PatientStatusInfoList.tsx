import { classNames } from "@/shared/lib/classNames";
import cls from "./PatientStatusInfoList.module.scss";
import type {
  PatientStatusItem,
  PatientStatusInfo,
} from "../../model/types/patientStatusInfo";
import { memo } from "react";

interface PatientStatusInfoListProps {
  className?: string;
  data: PatientStatusInfo;
}

const PatientStatusInfoListItem = memo((props: PatientStatusItem) => {
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

export const PatientStatusInfoList = memo(
  (props: PatientStatusInfoListProps) => {
    const { className, data } = props;

    return (
      <ul className={classNames(cls.PatientStatusInfoList, {}, [className])}>
        {data.map((item) => (
          <PatientStatusInfoListItem key={item.text} {...item} />
        ))}
      </ul>
    );
  },
);
