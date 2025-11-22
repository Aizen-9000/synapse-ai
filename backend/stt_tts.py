import io
import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


# -----------------------------
# 1) SPEECH → TEXT (Whisper STT)
# -----------------------------
async def transcribe_audio_file(file_bytes: bytes) -> str:
    """
    Transcribe audio to text using OpenAI Whisper.
    Works for Bengali, Hindi, all Indian languages.
    """
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY missing")
        return ""

    try:
        audio_file = io.BytesIO(file_bytes)

        result = client.audio.transcriptions.create(
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
    Returns audio in MP3 bytes.
    """
    if not OPENAI_API_KEY:
        print("OPENAI_API_KEY missing")
        return b""

    try:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",      # natural and stable voice
            input=text,
            format="mp3"
        )

        audio_bytes = response.read()  # binary MP3
        return audio_bytes

    except Exception as e:
        print("[TTS ERROR]", e)
        return b""