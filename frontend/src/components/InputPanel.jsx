import React, { useState } from "react";
import { startSpeechRecognition } from "../services/sttService";

const InputPanel = ({ onSend }) => {
  const [input, setInput] = useState("");
  const [listening, setListening] = useState(false);
  const [recognizer, setRecognizer] = useState(null);

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  const handleVoiceInput = () => {
    if (listening) {
      recognizer?.stop();
      setListening(false);
      return;
    }

    const recognition = startSpeechRecognition(
      (text) => setInput(text), // Update live text
      () => setListening(false), // End
      (err) => console.error("Speech error:", err)
    );

    if (recognition) {
      setRecognizer(recognition);
      setListening(true);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="input-panel">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={listening ? "Listening..." : "Type a message..."}
      />
      <button onClick={handleSend}>Send</button>
      <button
        onClick={handleVoiceInput}
        className={listening ? "mic-button active" : "mic-button"}
      >
        {listening ? "🎙️" : "🎤"}
      </button>
    </div>
  );
};

export default InputPanel;