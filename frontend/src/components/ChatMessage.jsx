import React, { useEffect, useRef, useState } from "react";

/**
 * Props:
 *  - message: { sender: "user" | "bot", text: string }
 */
const ChatMessage = ({ message }) => {
  const { sender, text } = message;
  const [speaking, setSpeaking] = useState(false);
  const utterRef = useRef(null);

  // Create and manage speech utterance
  const speak = async (textToSpeak) => {
    // If browser speech synthesis is not available, gracefully return
    if (!("speechSynthesis" in window) || !("SpeechSynthesisUtterance" in window)) {
      console.warn("Speech Synthesis not supported in this browser.");
      return;
    }

    // Stop any existing speech
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
    }

    const utter = new SpeechSynthesisUtterance(textToSpeak);
    utter.lang = "en-US"; // change if you want auto-detect or setting-driven lang
    utter.rate = 1; // speed (0.1 - 10)
    utter.pitch = 1; // pitch (0 - 2)
    // Optionally pick a voice (default will be used if not found)
    const voices = window.speechSynthesis.getVoices();
    if (voices && voices.length > 0) {
      // Try to pick a high-quality voice if available (browser dependent)
      const preferred = voices.find(v => v.lang.includes("en") && v.name.toLowerCase().includes("female")) || voices[0];
      if (preferred) utter.voice = preferred;
    }

    utter.onstart = () => setSpeaking(true);
    utter.onend = () => {
      setSpeaking(false);
      utterRef.current = null;
    };
    utter.onerror = (e) => {
      console.error("TTS error", e);
      setSpeaking(false);
      utterRef.current = null;
    };

    utterRef.current = utter;
    window.speechSynthesis.speak(utter);
  };

  const stopSpeak = () => {
    if (window.speechSynthesis && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
    }
    setSpeaking(false);
  };

  // Optional: auto-play bot messages (comment out if you prefer manual play)
  // useEffect(() => {
  //   if (sender === "bot" && text) {
  //     speak(text);
  //   }
  //   return () => {
  //     stopSpeak();
  //   }
  // }, [text, sender]);

  return (
    <div className={`chat-message ${sender}`}>
      <div className="message-text">{text}</div>

      {sender === "bot" && (
        <div className="tts-controls">
          <button
            className={`tts-play-btn ${speaking ? "speaking" : ""}`}
            onClick={() => {
              if (speaking) stopSpeak();
              else speak(text);
            }}
            title={speaking ? "Stop speaking" : "Play reply"}
          >
            {speaking ? "⏹️" : "🔊"}
          </button>
        </div>
      )}
    </div>
  );
};

export default ChatMessage;