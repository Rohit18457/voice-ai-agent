import logging
from typing import Optional
import speech_recognition as sr
from config import CALIBRATION_DURATION, PAUSE_THRESHOLD, ENERGY_THRESHOLD

logger = logging.getLogger(__name__)


class SpeechToTextEngine:
    """
    Speech-to-Text audio capture and transcription engine.
    Uses Google Web Speech API with adaptive noise calibration.
    """

    def __init__(
        self,
        calibration_duration: float = CALIBRATION_DURATION,
        pause_threshold: float = PAUSE_THRESHOLD,
        energy_threshold: int = ENERGY_THRESHOLD
    ):
        self.calibration_duration = calibration_duration
        self.pause_threshold = pause_threshold
        self.energy_threshold = energy_threshold

        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = self.pause_threshold
        if self.energy_threshold > 0:
            self.recognizer.energy_threshold = self.energy_threshold
            self.recognizer.dynamic_energy_threshold = True

    def calibrate(self, source: sr.Microphone):
        """Calibrate microphone sensitivity against background ambient noise."""
        try:
            self.recognizer.adjust_for_ambient_noise(source, duration=self.calibration_duration)
        except Exception as e:
            logger.warning(f"Ambient noise calibration warning: {e}")

    def listen_and_transcribe(self, source: sr.Microphone) -> Optional[str]:
        """
        Listen to audio from the microphone and return transcribed text.
        Returns None if speech is inaudible or unrecognized.
        """
        try:
            audio = self.recognizer.listen(source, phrase_time_limit=15)
            transcription = self.recognizer.recognize_google(audio)
            return transcription.strip()
        except sr.UnknownValueError:
            # User stayed quiet or speech was inaudible
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition network request failed: {e}")
            raise RuntimeError(f"Speech Recognition service unavailable: {e}")
        except Exception as e:
            logger.error(f"Unexpected audio capture error: {e}")
            return None
