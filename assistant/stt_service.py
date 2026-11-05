import io
import wave
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def transcribe_audio_bytes(audio_bytes, content_type='audio/wav'):
    """
    Transcribe raw audio bytes using:
    1. Google Gemini multimodal audio (if valid API key is present)
    2. SpeechRecognition Google Web Speech engine fallback
    """
    if not audio_bytes or len(audio_bytes) < 44:
        return ""

    # 1. Primary Engine: Google Gemini GenAI Multimodal Audio
    DEFAULT_GEMINI_KEY = 'AQ.Ab8RN6JjGb9DzxygCebSqJUlXxxe-vCKdmTJ2viUcsnYKsHVCA'
    api_key = getattr(settings, 'GEMINI_API_KEY', DEFAULT_GEMINI_KEY) or DEFAULT_GEMINI_KEY
    from .services import is_valid_api_key, get_gemini_client
    if is_valid_api_key(api_key):
        try:
            from google import genai
            from google.genai import types

            client = get_gemini_client()
            mime = content_type or ('audio/wav' if audio_bytes.startswith(b'RIFF') else 'audio/webm')
            audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime)
            response = client.models.generate_content(
                model=getattr(settings, 'GEMINI_MODEL', 'gemini-flash-lite-latest'),
                contents=[
                    audio_part,
                    "Transcribe the spoken audio verbatim. Output ONLY the raw spoken words with no preamble, formatting, quotes, or conversational explanations."
                ]
            )
            transcribed = (response.text or '').strip()
            # Clean any wrapping quotes or markdown formatting
            transcribed = transcribed.strip('"\'`')
            if transcribed:
                return transcribed
        except Exception as e:
            logger.warning("Gemini audio transcription notice: %s", str(e))

    # 2. Fallback Engine: SpeechRecognition with Google Web Speech
    try:
        import speech_recognition as sr
        r = sr.Recognizer()

        # If audio starts with RIFF (WAV file)
        if audio_bytes.startswith(b'RIFF'):
            with io.BytesIO(audio_bytes) as wav_file:
                with sr.AudioFile(wav_file) as source:
                    audio_data = r.record(source)
                    return r.recognize_google(audio_data)
        else:
            # Try recording as raw PCM if standard
            with io.BytesIO(audio_bytes) as wav_file:
                with sr.AudioFile(wav_file) as source:
                    audio_data = r.record(source)
                    return r.recognize_google(audio_data)
    except Exception as e:
        logger.warning("SpeechRecognition transcription fallback notice: %s", str(e))

    return ""

