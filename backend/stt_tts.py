import io
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()  # ensures .env is loaded
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


# -----------------------------
# 1) SPEECH → TEXT (Whisper STT)
# -----------------------------
async def transcribe_audio_file(file_bytes: bytes) -> str:
    """
    Transcribe audio to text using OpenAI Whisper.
    Supports all languages Whisper can detect.
    """
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY missing")
        return ""

    try:
        audio_file = io.BytesIO(file_bytes)

        # Use async create method
        result = await client.audio.transcriptions.acreate(
            model="whisper-1",
            file=audio_file,
        )

        return result.text

    except Exception as e:
        print("[STT ERROR]", e)
        return ""


# -----------------------------
# 2) TEXT → SPEECH (OpenAI TTS)
# -----------------------------
async def synthesize_tts(text: str) -> bytes:
    """
    Convert text to speech using OpenAI TTS.
    Model: gpt-4o-mini-tts
    Returns MP3 bytes.
    """
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY missing")
        return b""

    try:
        # Use async create method
        response = await client.audio.speech.acreate(
            model="gpt-4o-mini-tts",
            voice="alloy",      # natural and stable voice
            input=text,
            format="mp3"
        )

        # read() works for sync response; for async response, it should be .read()
        audio_bytes = response.read()
        return audio_bytes

    except Exception as e:
        print("[TTS ERROR]", e)
        return b""