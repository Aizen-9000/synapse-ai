from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router

app = FastAPI(title="Synapse.AI Backend")

origins = ["http://localhost","http://localhost:1420","tauri://localhost","http://127.0.0.1:1420","http://localhost:3000","*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

@app.get("/")
def root():
    return {"status":"Synapse.AI backend running","message":"Use /chat, /chat/stt, /chat/tts, /chat/translate"}