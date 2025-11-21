// frontend/src/services/ttsService.js

export const speakText = (text, voiceName = null, rate = 1) => {
  if (!window.speechSynthesis) {
    console.error("TTS not supported on this browser.");
    return;
  }

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = rate;

  if (voiceName) {
    const voices = window.speechSynthesis.getVoices();
    const selected = voices.find(v => v.name === voiceName);
    if (selected) utterance.voice = selected;
  }

  window.speechSynthesis.speak(utterance);
};