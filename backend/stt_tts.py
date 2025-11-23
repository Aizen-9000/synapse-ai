import io
import os
from openai import OpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


async def transcribe_audio_file(file_bytes: bytes) -> str:
    if not OPENAI_API_KEY:
        print("[STT] No API key")
        return ""

    try:
        audio = io.BytesIO(file_bytes)

        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", audio, "audio/wav")
        )

        print("[WHISPER RAW RESPONSE]", resp)
        return resp.text or ""

    except Exception as e:
        print("[STT ERROR]", e)
        return ""


async def synthesize_tts(text: str, voice: str = "alloy") -> bytes:
    # First try ElevenLabs
    if ELEVENLABS_API_KEY:
        try:
            url = "https://api.elevenlabs.io/v1/text-to-speech/default"
            headers = {
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {"text": text}
            r = requests.post(url, json=payload, headers=headers)

            if r.status_code == 200:
                return r.content
        except Exception as e:
            print("[TTS ERROR ElevenLabs]", e)

    # Fallback OpenAI TTS
    if OPENAI_API_KEY:
        try:
            response = await client.audio.speech.acreate(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
                format="mp3"
            )
            return response.read()
        except Exception as e:
            print("[TTS ERROR OpenAI]", e)

    return b""