import React, { useState } from "react";
import ChatContainer from "./ChatContainer";
import InputPanel from "./InputPanel";
import { sendMessage } from "../services/chatService";

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);

  const handleSend = async (text) => {
    if (!text.trim()) return;

    const userMsg = { sender: "user", text };
    setMessages((prev) => [...prev, userMsg]);

    // Temporary bot message placeholder
    const botMsg = { sender: "bot", text: "" };
    setMessages((prev) => [...prev, botMsg]);

    let botIndex = -1;

    setMessages((prev) => {
      botIndex = prev.length;
      return prev;
    });

    // Streaming
    await sendMessage(text, (partial) => {
      setMessages((prev) => {
        const updated = [...prev];
        updated[botIndex] = { sender: "bot", text: partial };
        return updated;
      });
    });
  };

  return (
    <div className="chat-window">
      <ChatContainer messages={messages} />
      <InputPanel onSend={handleSend} />
    </div>
  );
};

export default ChatWindow;