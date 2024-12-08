import cls from "./MessageBubble.module.scss";
import type { Message } from "../../model/types";
import { classNames } from "@/shared/lib/classNames";

interface MessageBubbleProps {
  className?: string;
  message: Message;
}

export const MessageBubble = (props: MessageBubbleProps) => {
  const { message, className } = props;
  return (
    <div
      className={classNames(cls.MessageBubble, {}, [
        className,
        cls[message.source],
      ])}
    >
      <p>{message.text}</p>
      <span className={cls.date}>{message.date}</span>
    </div>
  );
};
