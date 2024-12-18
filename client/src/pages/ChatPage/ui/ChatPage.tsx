import { useState } from "react";
import cls from "./ChatPage.module.scss";
import {
  ChatContacts,
  ChatDialog,
  type Contact,
  type Message,
} from "@/features/ChatPanel";
import { Page } from "@/widgets/Page";
import { NotePanel } from "@/features/NotePanel";

export const mockContacts: Contact[] = [
  {
    id: "1",
    name: "Ivan Ivanov",
    lastMessage: "Hello! The results will be ready tomorrow.",
    avatar: "https://poloskun-shop.ru/wp-content/uploads/2021/07/gPZwCbdS.jpg",
  },
  {
    id: "2",
    name: "Anna Smirnova",
    lastMessage: "Please remind me about the medications. How many times...",
    avatar: "https://cdn1.flamp.ru/2af703592e4212ae59e420a39c0a7dca.jpg",
  },
];

export const mockMessages: Record<string, Message[]> = {
  "1": [
    { id: "m1", source: "receiver", text: "Hello!", date: "12/09/2024" },
    {
      id: "m2",
      source: "receiver",
      text: "How long will the results take?",
      date: "12/09/2024",
    },
    {
      id: "m3",
      source: "sender",
      text: "Hello! The results will be ready tomorrow.",
      date: "12/09/2024",
    },
  ],
  "2": [
    {
      id: "m4",
      source: "receiver",
      text: "Good afternoon!",
      date: "12/08/2024",
    },
    {
      id: "m5",
      source: "sender",
      text: "Good afternoon! How can I help you?",
      date: "12/08/2024",
    },
    {
      id: "m6",
      source: "receiver",
      text: "Please remind me about the medications. How many times a day should Respiphorb be taken?",
      date: "12/08/2024",
    },
  ],
};

export const ChatPage = () => {
  const [selectedContactId, setSelectedContactId] = useState<string>("1");
  const [messages, setMessages] = useState(mockMessages);

  const handleSelectContact = (id: string) => {
    setSelectedContactId(id);
  };

  const handleSendMessage = (message: string) => {
    if (!selectedContactId) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      source: "sender",
      text: message,
      date: new Date().toLocaleDateString(),
    };

    setMessages((prev) => ({
      ...prev,
      [selectedContactId]: [...prev[selectedContactId], newMessage],
    }));
  };

  const selectedContact = mockContacts.find((c) => c.id === selectedContactId);
  return (
    <Page>
      <div className={cls.chatContainer}>
        <div className={cls.contacts}>
          <ChatContacts
            selectedContactId={selectedContactId}
            contacts={mockContacts}
            onSelectContact={handleSelectContact}
          />
          <NotePanel />
        </div>
        <div className={cls.chat}>
          {selectedContact ? (
            <ChatDialog
              contact={selectedContact}
              messages={messages[selectedContactId]}
              onSendMessage={handleSendMessage}
            />
          ) : (
            <div className={cls.placeholder}>
              Выберите контакт для начала диалога
            </div>
          )}
        </div>
      </div>
    </Page>
  );
};
