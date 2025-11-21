from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import chat, users

app = FastAPI(title="Synapse AI Backend")
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"status": "ok", "app": "Synapse AI Backend"}