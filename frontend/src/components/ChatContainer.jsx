import React, { useState } from "react";
import ChatWindow from "./ChatWindow";
import InputPanel from "./InputPanel";
import Header from "./Header";
import SettingsModal from "./SettingsModal";
import { sendMessage } from "../services/chatService";

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [showSettings, setShowSettings] = useState(false);

  const handleSend = async (userMessage) => {
    // Show user message immediately
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);

    try {
      // Ask backend for response
      const reply = await sendMessage(userMessage);
      setMessages((prev) => [...prev, { sender: "bot", text: reply }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "[Error: could not get response]" },
      ]);
    }
  };

  return (
    <div className="chat-container">
      <Header onSettingsClick={() => setShowSettings(true)} />
      <ChatWindow messages={messages} />
      <InputPanel onSend={handleSend} />
      {showSettings && <SettingsModal onClose={() => setShowSettings(false)} />}
    </div>
  );
};

export default ChatContainer;