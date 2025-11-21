import json
import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(payload: dict):
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="No message provided")

    def stream_ollama():
        try:
            with requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={"model": "llama3", "prompt": message},
                stream=True,
            ) as response:
                if response.status_code != 200:
                    yield json.dumps({"error": "Ollama API error"}) + "\n"
                    return

                for line in response.iter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line.decode("utf-8"))
                        # ✅ Only send "response" parts (the text tokens)
                        if "response" in data:
                            yield json.dumps({"response": data["response"]}) + "\n"
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    # ✅ Send as text stream
    return StreamingResponse(stream_ollama(), media_type="text/event-stream")