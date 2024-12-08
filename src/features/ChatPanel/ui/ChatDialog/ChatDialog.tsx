import cls from "./ChatDialog.module.scss";
import { MessageBubble } from "../MessageBubble/MessageBubble";
import { MessageInput } from "../MessageInput/MessageInput";
import type { Contact, Message } from "../../model/types";
import { classNames } from "@/shared/lib/classNames";

interface ChatDialogProps {
  className?: string;
  contact: Contact;
  messages: Message[];
  onSendMessage: (message: string) => void;
}

export const ChatDialog = (props: ChatDialogProps) => {
  const { className, contact, messages, onSendMessage } = props;
  return (
    <div className={classNames(cls.ChatDialog, {}, [className])}>
      <div className={cls.header}>
        <h3>{contact.name}</h3>
      </div>
      <div className={cls.messages}>
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            message={msg}
            className={cls.messageBubble}
          />
        ))}
      </div>
      <div className={cls.inputContainer}>
        <MessageInput onSendMessage={onSendMessage} />
      </div>
    </div>
  );
};
