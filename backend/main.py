from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router
from backend.routes.users import router as users_router

app = FastAPI(title="Synapse.AI Backend")

# Allowed origins for both dev & production (Tauri)
origins = [
    "http://localhost",
    "http://localhost:1420",     # Tauri dev
    "tauri://localhost",         # Tauri production
    "http://127.0.0.1:1420",
    "http://localhost:3000",
    "*"                          # fallback -> can remove later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach all routers
app.include_router(chat_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {
        "status": "Synapse.AI backend running",
        "message": "Use /chat, /chat/stt, /chat/tts, /chat/search"
    }