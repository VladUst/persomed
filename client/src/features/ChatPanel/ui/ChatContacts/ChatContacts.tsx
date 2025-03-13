import cls from "./ChatContacts.module.scss";
import List from "@mui/material/List";
import ListItemText from "@mui/material/ListItemText";
import type { Contact } from "../../model/types";
import { Avatar, Divider, ListItemAvatar, ListItemButton } from "@mui/material";
import { classNames } from "@/shared/lib/classNames";

interface ChatContactsProps {
  className?: string;
  contacts: Contact[];
  selectedContactId: string;
  onSelectContact: (id: string) => void;
}

export const ChatContacts = (props: ChatContactsProps) => {
  const { className, contacts, selectedContactId, onSelectContact } = props;
  return (
    <div className={classNames(cls.ChatContacts, {}, [className])}>
      <List>
        {contacts.map((contact) => (
          <div key={contact.id}>
            <ListItemButton
              selected={selectedContactId === contact.id}
              onClick={() => onSelectContact(contact.id)}
            >
              <ListItemAvatar>
                <Avatar alt="Remy Sharp" src={contact.avatar} />
              </ListItemAvatar>
              <ListItemText
                primary={contact.name}
                secondary={contact.lastMessage}
              />
            </ListItemButton>
            <Divider variant="fullWidth" component="li" />
          </div>
        ))}
      </List>
    </div>
  );
};
