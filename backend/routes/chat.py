# backend/routes/chat.py

from fastapi import APIRouter, HTTPException, Body, File, UploadFile
from backend.llm_adapter import llm
from backend import web_search
from backend.stt_tts import transcribe_audio_file, synthesize_tts
from typing import Optional

router = APIRouter(prefix="/chat", tags=["Chat"])

# ---------------------------
# 1. MAIN CHAT ENDPOINT
# ---------------------------
@router.post("/")
async def chat(payload: dict = Body(...)):
    """
    payload:
    {
      "message": "...",
      "model": "optional",
      "web": true/false
    }
    """
    prompt: str = payload.get("message", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="No message provided")

    model_name: Optional[str] = payload.get("model")
    use_web: bool = bool(payload.get("web", False))

    try:
        sources = []

        # Optional web search
        if use_web:
            try:
                sources = web_search.search_web(prompt)
            except Exception as e:
                print("Websearch error:", e)
                sources = []

        # Inject web search results into LLM prompt if available
        final_prompt = prompt
        if sources:
            src_text = "\n".join([
                f"{i+1}. {s.get('title')} - {s.get('link')}\n{ s.get('snippet','') }"
                for i, s in enumerate(sources[:5])
            ])

            final_prompt = (
                f"{prompt}\n\n"
                f"Web search results:\n{src_text}\n\n"
                f"Use these results to answer clearly. Cite sources if needed."
            )

        reply = await llm.generate(final_prompt, model=model_name)

        return {
            "response": reply,
            "sources": sources
        }

    except Exception as e:
        print("LLM error:", str(e))
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


# ---------------------------
# 2. TRANSLATION ENDPOINT
# ---------------------------
@router.post("/translate")
async def translate_text(payload: dict = Body(...)):
    """
    payload:
    {
        "text": "...",
        "target_lang": "bn"  # or Hindi, Tamil, etc.
    }
    """
    text = payload.get("text")
    target = payload.get("target_lang")

    if not text or not target:
        raise HTTPException(status_code=400, detail="text and target_lang required")

    try:
        prompt = (
            f"Translate the following into '{target}'. "
            f"Respond ONLY with the translated text, no explanations.\n\n{text}"
        )
        translated = await llm.generate(prompt)
        return {"translation": translated}
    except Exception as e:
        print("Translate error:", e)
        raise HTTPException(status_code=500, detail=f"Translate error: {str(e)}")


# ---------------------------
# 3. SPEECH-TO-TEXT (ANY LANGUAGE)
# ---------------------------
@router.post("/stt")
async def stt_endpoint(file: UploadFile = File(...)):
    """
    Accepts audio from frontend stt-service.js
    """
    try:
        text = await transcribe_audio_file(file)
        return {"text": text}
    except Exception as e:
        print("STT error:", e)
        raise HTTPException(status_code=500, detail=f"STT error: {str(e)}")


# ---------------------------
# 4. TEXT-TO-SPEECH (MULTILINGUAL)
# ---------------------------
@router.post("/tts")
async def tts_endpoint(payload: dict = Body(...)):
    """
    payload:
    {
        "text": "...",
        "lang": "hi" or "bn" or "en"
    }
    """
    text = payload.get("text")
    lang = payload.get("lang", "en")

    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    try:
        audio_bytes = await synthesize_tts(text, lang)
        return {
            "audio": audio_bytes.hex()  # hex encode for JSON
        }
    except Exception as e:
        print("TTS error:", e)
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")