import logging
from typing import Optional, List
from config import TTS_RATE, TTS_VOLUME, TTS_VOICE_INDEX

logger = logging.getLogger(__name__)


class TextToSpeechEngine:
    """
    Offline Text-to-Speech Engine using pyttsx3.
    Provides fast, zero-latency local speech synthesis without cloud costs.
    """

    def __init__(
        self,
        rate: int = TTS_RATE,
        volume: float = TTS_VOLUME,
        voice_index: int = TTS_VOICE_INDEX
    ):
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index
        self.engine = None
        self.is_available = False

        self._init_engine()

    def _init_engine(self):
        """Initialize the pyttsx3 engine and configure voice properties."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.rate)
            self.engine.setProperty("volume", self.volume)

            # Configure voice if available
            voices = self.engine.getProperty("voices")
            if voices and len(voices) > self.voice_index:
                self.engine.setProperty("voice", voices[self.voice_index].id)

            self.is_available = True
        except ImportError:
            logger.warning("pyttsx3 is not installed. Run 'pip install pyttsx3' for voice playback.")
            self.is_available = False
        except Exception as e:
            logger.error(f"Failed to initialize pyttsx3: {e}")
            self.is_available = False

    def speak(self, text: str):
        """
        Synthesize and speak text aloud.
        """
        clean_text = text.strip()
        if not clean_text:
            return

        if self.is_available and self.engine:
            try:
                self.engine.say(clean_text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS playback error: {e}")
        else:
            print("\n[Audio Out] (Install 'pyttsx3' to hear audio aloud)")

    def get_available_voices(self) -> List[str]:
        """Return list of voice names installed on the host OS."""
        if not self.is_available or not self.engine:
            return []
        try:
            voices = self.engine.getProperty("voices")
            return [v.name for v in voices]
        except Exception:
            return []
