import React, { useEffect, useState } from "react";

const SettingsModal = ({ onClose, onSave }) => {
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState("");
  const [rate, setRate] = useState(1);

  useEffect(() => {
    const loadVoices = () => setVoices(window.speechSynthesis.getVoices());
    loadVoices();
    window.speechSynthesis.onvoiceschanged = loadVoices;
  }, []);

  return (
    <div className="settings-modal">
      <div className="settings-content">
        <h3>Voice Settings</h3>

        <label>Voice:</label>
        <select value={selectedVoice} onChange={(e) => setSelectedVoice(e.target.value)}>
          <option value="">Default</option>
          {voices.map((v, i) => (
            <option key={i} value={v.name}>{v.name} ({v.lang})</option>
          ))}
        </select>

        <label>Speed: {rate.toFixed(1)}</label>
        <input
          type="range"
          min="0.5"
          max="1.5"
          step="0.1"
          value={rate}
          onChange={(e) => setRate(parseFloat(e.target.value))}
        />

        <div className="settings-actions">
          <button onClick={() => onSave({ voice: selectedVoice, rate })}>Save</button>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;