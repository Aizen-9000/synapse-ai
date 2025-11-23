from fastapi import APIRouter, HTTPException, Body, File, UploadFile
from typing import Optional
from backend.llm_adapter import llm
from backend import web_search
from backend.stt_tts import transcribe_audio_file, synthesize_tts

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(payload: dict = Body(...)):
    prompt = payload.get("message","")
    if not prompt: raise HTTPException(400,"No message provided")
    model_name: Optional[str] = payload.get("model")
    use_web = bool(payload.get("web", False))
    try:
        sources = []
        if use_web:
            try: sources = web_search.search_web(prompt)
            except: sources=[]
        final_prompt = prompt
        if sources:
            src_text = "\n".join([f"{i+1}. {s.get('title')} - {s.get('link')}\n{s.get('snippet','')}" for i,s in enumerate(sources[:5])])
            final_prompt = f"{prompt}\n\nWeb search results:\n{src_text}\n\nUse these results to answer clearly. Cite sources if needed."
        reply = await llm.generate(final_prompt, model=model_name)
        return {"response": reply, "sources": sources}
    except Exception as e:
        raise HTTPException(500,f"Chat error: {str(e)}")

@router.post("/translate")
async def translate_text(payload: dict = Body(...)):
    text = payload.get("text")
    target = payload.get("target_lang")
    if not text or not target: raise HTTPException(400,"text and target_lang required")
    try:
        prompt = f"Translate the following into '{target}'. Respond ONLY with the translated text, no explanations.\n\n{text}"
        translated = await llm.generate(prompt)
        return {"translation": translated}
    except Exception as e:
        raise HTTPException(500,f"Translate error: {str(e)}")

@router.post("/stt")
async def stt_endpoint(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = await transcribe_audio_file(file_bytes)
        return {"text": text}
    except Exception as e:
        raise HTTPException(500,f"STT error: {str(e)}")

@router.post("/tts")
async def tts_endpoint(payload: dict = Body(...)):
    text = payload.get("text")
    lang = payload.get("lang","en")
    if not text: raise HTTPException(400,"No text provided")
    try:
        audio_bytes = await synthesize_tts(text)
        return {"audio": audio_bytes.hex()}
    except Exception as e:
        raise HTTPException(500,f"TTS error: {str(e)}")