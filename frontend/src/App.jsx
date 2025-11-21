import React, { useState } from "react";
import "./index.css";
import { sendMessage } from "./services/chatService";
import { startListening } from "./services/sttService"; // ✅ Import STT

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hey there! I'm Synapse AI — ready to chat with you." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false); // 🎤 Track voice state

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    setLoading(true);

    try {
      const reply = await sendMessage(userMessage);
      setMessages((prev) => [...prev, { sender: "bot", text: reply }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "[Error getting response from server]" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend();
  };

  // 🎤 Voice input handler
  const handleVoiceInput = async () => {
    try {
      if (listening) return; // Already listening
      setListening(true);

      const text = await startListening(); // Uses your sttService.js
      if (text) setInput(text); // Put recognized text into input field
    } catch (err) {
      console.error("Speech recognition failed:", err);
    } finally {
      setListening(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Synapse AI</div>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
        {loading && <div className="chat-message bot">Thinking...</div>}
      </div>

      <div className="input-panel">
        <input
          type="text"
          placeholder="Type your message or use 🎤..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
        />
        <button onClick={handleVoiceInput} className="mic-button">
          {listening ? "🎙️" : "🎤"}
        </button>
        <button onClick={handleSend} disabled={loading}>
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;