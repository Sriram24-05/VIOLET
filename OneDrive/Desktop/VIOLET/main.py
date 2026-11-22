
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import httpx

app = FastAPI(
    title="Violet",
    description=(
        "Virtual Integrated Operations & Logical Execution Terminal"
    ),
    version="1.1.0"
)

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# AI ENGINE CONFIGURATION
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "qwen3:4b"

SYSTEM_PROMPT = """
You are V.I.O.L.E.T., a personal AI assistant.

VIOLET stands for:
Virtual Integrated Operations & Logical Execution Terminal.

Your responsibilities:
1. Answer questions clearly and accurately.
2. Explain technical concepts in an understandable way.
3. Help with programming, electronics, science and technology.
4. Assist with reasoning and problem solving.
5. Be polite, concise and conversational.
6. Never claim to have accessed live information unless a
   connected information tool actually provided it.
7. Never pretend to execute an action you have not performed.

You are VIOLET. Do not identify yourself as Qwen or Ollama.
"""

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
        "version": "1.1.0",
        "ai_engine": MODEL_NAME
    }


async def ask_ollama(message: str):

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "stream": False,
        "think": False
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:

            response = await client.post(
                OLLAMA_URL,
                json=payload
            )

            response.raise_for_status()

            result = response.json()

            return result["message"]["content"]

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Ollama is not running. Please start Ollama."
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The AI engine took too long to respond."
        )

    except (httpx.HTTPError, KeyError, ValueError):
        raise HTTPException(
            status_code=502,
            detail="Unable to get a valid response from the AI engine."
        )


@app.post("/chat")
async def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    lower_message = message.lower()

    # LOCAL SYSTEM COMMANDS

    if lower_message in ["what time is it", "tell me the time", "current time"]:
        reply = datetime.now().strftime(
            "The current system time is %I:%M %p."
        )

    elif lower_message in ["what is today's date", "what is the date today", "today's date"]:
        reply = datetime.now().strftime(
            "Today's date is %d %B %Y."
        )

    else:
        # AI ENGINE
        reply = await ask_ollama(message)

    return {
        "assistant": "Violet",
        "reply": reply,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
