import io
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

async def transcribe_audio_file(file_bytes: bytes) -> str:
    if not OPENAI_API_KEY: return ""
    try:
        audio_file = io.BytesIO(file_bytes)
        result = await client.audio.transcriptions.acreate(model="whisper-1", file=audio_file)
        return result.text
    except Exception as e:
        print("[STT ERROR]", e)
        return ""

async def synthesize_tts(text: str) -> bytes:
    if not OPENAI_API_KEY: return b""
    try:
        response = await client.audio.speech.acreate(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
            format="mp3"
        )
        return response.read()
    except Exception as e:
        print("[TTS ERROR]", e)
        return b""