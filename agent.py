import time
from typing import Callable, Optional
import speech_recognition as sr
from core.stt import SpeechToTextEngine
from core.tts import TextToSpeechEngine
from core.llm import ConversationalAgent


class VoiceAgent:
    """
    Main Voice Agent orchestrator managing the full pipeline:
    Microphone Audio -> Speech-To-Text -> Groq LLM -> Text-To-Speech -> Speaker Audio
    """

    EXIT_KEYWORDS = {"exit", "quit", "stop", "bye", "goodbye", "terminate", "close"}

    def __init__(
        self,
        stt_engine: Optional[SpeechToTextEngine] = None,
        tts_engine: Optional[TextToSpeechEngine] = None,
        llm_agent: Optional[ConversationalAgent] = None
    ):
        self.stt = stt_engine or SpeechToTextEngine()
        self.tts = tts_engine or TextToSpeechEngine()
        self.llm = llm_agent or ConversationalAgent()

    def process_turn(
        self,
        user_text: str,
        on_response: Optional[Callable[[str, float], None]] = None
    ) -> str:
        """
        Process a transcribed user turn:
        1. Append to conversational history.
        2. Generate LLM completion via Groq.
        3. Speak response aloud via TTS.
        """
        start_time = time.perf_counter()

        self.llm.add_user_message(user_text)
        ai_response = self.llm.generate_response()
        self.llm.add_assistant_message(ai_response)

        latency = time.perf_counter() - start_time

        if on_response:
            on_response(ai_response, latency)

        # Synthesize and speak audio
        self.tts.speak(ai_response)

        return ai_response

    def is_exit_command(self, text: str) -> bool:
        """Check if user uttered a shutdown/exit command."""
        clean = text.lower().strip().rstrip(".!?")
        return clean in self.EXIT_KEYWORDS or any(
            clean.startswith(kw) for kw in ["please exit", "please stop", "say goodbye"]
        )

