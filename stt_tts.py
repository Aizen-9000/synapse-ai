import io
from openai import OpenAI
from .config import settings

async def transcribe_audio_file(file_bytes: bytes) -> str:
    if settings.OPENAI_API_KEY:
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
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
    if settings.ELEVENLABS_API_KEY:
        try:
            import requests
            url = "https://api.elevenlabs.io/v1/text-to-speech/default"
            headers = {"xi-api-key": settings.ELEVENLABS_API_KEY, "Content-Type": "application/json"}
            payload = {"text": text}
            r = requests.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                return r.content
        except Exception as e:
            print("[TTS ERROR]", e)
    return b""