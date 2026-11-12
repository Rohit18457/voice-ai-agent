import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("[Error] GROQ_API_KEY is not set. Please add it to your .env file.")
    sys.exit(1)

GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")

# Audio / Speech Recognition Configuration
CALIBRATION_DURATION = float(os.getenv("CALIBRATION_DURATION", "1.0"))
PAUSE_THRESHOLD = float(os.getenv("PAUSE_THRESHOLD", "1.5"))
ENERGY_THRESHOLD = int(os.getenv("ENERGY_THRESHOLD", "300"))

# Text-to-Speech (TTS) Configuration
TTS_RATE = int(os.getenv("TTS_RATE", "175"))
TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))
TTS_VOICE_INDEX = int(os.getenv("TTS_VOICE_INDEX", "0"))

# Conversational Agent System Persona
DEFAULT_SYSTEM_PROMPT = """You are an intelligent, empathetic, and expert voice AI assistant.
You receive transcripts of what the user speaks aloud.
Guidelines for your responses:
- Speak in a natural, friendly, and engaging conversational tone.
- Keep your answers concise, clear, and direct (1 to 3 sentences maximum).
- Avoid bullet points, code blocks, or markdown tables unless specifically asked, as your response will be read aloud to the user.
- If the user asks for code or long explanations, summarize the key concept verbally first.
"""

