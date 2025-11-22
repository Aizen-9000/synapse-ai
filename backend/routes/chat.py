from fastapi import APIRouter, HTTPException, Body
from backend.llm_adapter import llm

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(payload: dict = Body(...)):
    prompt = payload.get("message", "")
    if not prompt:
        raise HTTPException(status_code=400, detail="No message provided")

    model_name = payload.get("model")  # optional key from frontend
    try:
        print("Prompt received:", prompt)
        grok_reply = await llm.generate(prompt, model=model_name)
        print("GROK AI reply:", grok_reply)
    except Exception as e:
        print("Error calling GROK AI:", str(e))
        raise HTTPException(status_code=500, detail=f"GROK AI error: {str(e)}")

    return {"response": grok_reply}