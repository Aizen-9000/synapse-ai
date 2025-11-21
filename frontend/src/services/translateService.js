import axios from "axios";

// Use environment variable for backend URL
const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

/**
 * Translate a given text to a target language using backend API.
 * @param {string} text - Text to translate
 * @param {string} targetLang - Language code to translate into
 * @returns {Promise<string>} - Translated text or error string
 */
export const translateText = async (text, targetLang) => {
  try {
    const res = await axios.post(`${API_URL}/chat/translate`, {
      text,
      target_lang: targetLang,
    });

    if (res.data && res.data.translation) {
      return res.data.translation;
    }

    return "[Translation error: no translation returned]";
  } catch (err) {
    console.error("[TranslateService Error]:", err);
    return "[Error translating text]";
  }
};