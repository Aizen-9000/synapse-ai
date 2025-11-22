import io
import os
from openai import OpenAI

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


async def transcribe_audio_file(file_bytes: bytes) -> str:
    """
    Transcribe audio using OpenAI Whisper API.
    """
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


async def synthesize_tts(text: str) -> bytes:
    """
    Convert text to speech using ElevenLabs API.
    """
    if not ELEVENLABS_API_KEY:
        return b""

    try:
        import requests

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
        print("[TTS ERROR]", e)

    return b""