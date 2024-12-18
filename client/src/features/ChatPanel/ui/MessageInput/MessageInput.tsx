import { useState } from "react";
import cls from "./MessageInput.module.scss";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import SendIcon from "@mui/icons-material/Send";
import { classNames } from "@/shared/lib/classNames";

interface MessageInputProps {
  className?: string;
  onSendMessage: (message: string) => void;
}

export const MessageInput = (props: MessageInputProps) => {
  const { className, onSendMessage } = props;
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <div className={classNames(cls.MessageInput, {}, [className])}>
      <TextField
        fullWidth
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Enter a message..."
      />
      <IconButton onClick={handleSend} color="primary">
        <SendIcon />
      </IconButton>
    </div>
  );
};
