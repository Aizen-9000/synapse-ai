# backend/stt_tts.py
import io
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# STT using OpenAI Whisper
def transcribe_audio_file(file_bytes: bytes) -> str:
    if not OPENAI_API_KEY:
        return ""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        audio_file = io.BytesIO(file_bytes)
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return resp.text
    except Exception as e:
        print("[STT ERROR]", e)
        return ""

# TTS using ElevenLabs
def synthesize_tts(text: str) -> bytes:
    if not ELEVENLABS_API_KEY:
        return b""
    try:
        url = "https://api.elevenlabs.io/v1/text-to-speech/default"
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"text": text}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            print("[TTS ERROR] Status:", response.status_code, response.text)
    except Exception as e:
        print("[TTS ERROR]", e)
    return b""