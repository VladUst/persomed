import React, { memo } from "react";

import cls from "./Icon.module.scss";
import { classNames } from "@/shared/lib/classNames";

interface IconProps extends React.SVGProps<SVGSVGElement> {
  className?: string;
  Svg: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  secondary?: boolean;
}

export const Icon = memo((props: IconProps) => {
  const { className, Svg, secondary, ...otherProps } = props;

  return (
    <Svg
      className={classNames(secondary ? cls.secondary : cls.Icon, {}, [
        className,
      ])}
      {...otherProps}
    />
  );
});
