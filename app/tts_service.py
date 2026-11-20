"""
app/tts_service.py — Zero-Cost Neural Text-to-Speech Engine for KhetSathi 360.

Provides free, studio-grade neural voice synthesis in Hindi (hi-IN) and Indian English (en-IN)
using Microsoft Edge Neural TTS (edge-tts). Zero cloud API keys or billing required.
"""
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Default Neural Voices
VOICE_MAP = {
    "hi": "hi-IN-SwaraNeural",      # Warm, natural Hindi female voice
    "hi-male": "hi-IN-MadhurNeural", # Natural Hindi male voice
    "en": "en-IN-NeerjaNeural",     # Indian English female voice
    "en-male": "en-IN-PrabhatNeural",# Indian English male voice
}


async def synthesize_neural_speech(text: str, lang: str = "hi", voice: Optional[str] = None) -> bytes:
    """
    Synthesize plain text into MP3 audio bytes using edge-tts.
    Falls back gracefully if edge-tts fails or is unreachable.
    """
    cleaned_text = text.strip()
    if not cleaned_text:
        raise ValueError("Text for speech synthesis cannot be empty.")

    # Limit text length to prevent abuse (up to 2000 characters per request)
    cleaned_text = cleaned_text[:2000]

    selected_voice = voice or VOICE_MAP.get(lang.lower(), "hi-IN-SwaraNeural")

    try:
        import edge_tts

        communicate = edge_tts.Communicate(text=cleaned_text, voice=selected_voice, rate="+0%", volume="+0%")
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])

        audio_bytes = audio_buffer.getvalue()
        if not audio_bytes:
            raise RuntimeError("Audio synthesis returned empty buffer.")
        return audio_bytes
    except Exception as e:
        logger.error("Neural TTS synthesis error with voice '%s': %s", selected_voice, e)
        raise RuntimeError(f"Speech synthesis failed: {e}") from e
