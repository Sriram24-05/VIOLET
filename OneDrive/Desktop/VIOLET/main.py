
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

app = FastAPI(
    title="Violet",
    description=(
        "Virtual Integrated Operations & Logical Execution Terminal"
    ),
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {
        "status": "Violet online",
        "system": "Virtual Integrated Operations & Logical Execution Terminal",
        "version": "1.0.0"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.lower().strip()

    if message in ["hello", "hi", "hey"]:
        reply = (
            "Hello! I am Violet, your personal "
            "AI assistant. How may I assist you?"
        )

    elif "your name" in message or "who are you" in message:
        reply = (
            "I am Violet, your personal AI assistant. "
            "Violet stands for Virtual Integrated Operations "
            "& Logical Execution Terminal."
        )

    elif "time" in message:
        now = datetime.now().strftime("%I:%M %p")
        reply = f"The current system time is {now}."

    elif "date" in message or "today" in message:
        today = datetime.now().strftime("%d %B %Y")
        reply = f"Today's date is {today}."

    elif "how are you" in message or "system status" in message:
        reply = (
            "All systems are operational. "
            "Violet is online and ready for your commands."
        )

    elif "help" in message or "what can you do" in message:
        reply = (
            "I can respond to greetings, identify myself, "
            "tell you the current time and date, and report "
            "my system status. More capabilities can be added "
            "as the system develops."
        )

    elif "thank" in message:
        reply = "You're welcome! I'm always ready to assist."

    elif "good morning" in message:
        reply = "Good morning! Violet is online and ready."

    elif "good night" in message:
        reply = "Good night! Violet signing off."

    else:
        reply = (
            "Command received. I understand your message, "
            "but my advanced AI engine is not connected yet."
        )

    return {
        "assistant": "Violet",
        "reply": reply,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
