export interface Message {
  id: string;
  source: "sender" | "receiver";
  text: string;
  date: string;
}

export interface Contact {
  id: string;
  name: string;
  lastMessage: string;
  avatar: string;
}
