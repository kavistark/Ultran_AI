import asyncio
import io
import os
import tempfile
import logging
import concurrent.futures

logger = logging.getLogger(__name__)

# Single Dedicated Villain Voice Configuration for AI ULTRON
EDGE_VOICE = "en-US-ChristopherNeural"
EDGE_PITCH = "-16Hz"   # Deep menacing villain baritone shift
EDGE_RATE = "-7%"      # Cold, calculated, deliberate cadence


async def _synthesize_edge_tts(text, voice=EDGE_VOICE, pitch=EDGE_PITCH, rate=EDGE_RATE):
    """Synthesize natural neural speech using edge-tts."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
    buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buffer.write(chunk["data"])
    buffer.seek(0)
    return buffer.read(), "audio/mpeg"


def _synthesize_pyttsx3(text):
    """Offline computer speech fallback using pyttsx3 with thread-safe COM init."""
    co_initialized = False
    try:
        import pythoncom
        pythoncom.CoInitialize()
        co_initialized = True
    except Exception:
        pass

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tf:
        temp_path = tf.name

    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        voices = engine.getProperty('voices')
        # Select deepest male voice (usually Microsoft David)
        for v in voices:
            if 'david' in v.name.lower() or 'male' in v.name.lower():
                engine.setProperty('voice', v.id)
                break
        engine.save_to_file(text, temp_path)
        engine.runAndWait()

        with open(temp_path, 'rb') as f:
            data = f.read()
        return data, "audio/wav"
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        if co_initialized:
            try:
                import pythoncom
                pythoncom.CoUninitialize()
            except Exception:
                pass


def _safe_run_async(coro):
    """Execute coroutine safely even if an asyncio loop is active in the current thread."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


_SPEECH_CACHE = {}
_MAX_CACHE_ENTRIES = 128


def generate_deep_cinematic_speech(text, engine="edge-tts"):
    """
    Generate deep cinematic neural speech for AI ULTRON.
    Tries edge-tts natural neural voices first, then pyttsx3 offline speech.
    Uses an in-memory cache to eliminate synthesis latency on repeated phrases.
    """
    clean = text.strip()
    if not clean:
        return b"", "audio/mpeg"

    cache_key = (clean, engine)
    if cache_key in _SPEECH_CACHE:
        return _SPEECH_CACHE[cache_key]

    result = None
    # 1. Edge-TTS (Natural Neural Deep Voice)
    try:
        result = _safe_run_async(_synthesize_edge_tts(clean))
    except Exception as e:
        logger.warning(f"edge-tts synthesis note: {e}, falling back to pyttsx3.")

    # 2. Pyttsx3 (Offline Computer Speech)
    if not result or not result[0]:
        try:
            result = _synthesize_pyttsx3(clean)
        except Exception as e:
            logger.error(f"pyttsx3 fallback error: {e}")
            result = (b"", "audio/mpeg")

    if result and result[0]:
        if len(_SPEECH_CACHE) >= _MAX_CACHE_ENTRIES:
            _SPEECH_CACHE.pop(next(iter(_SPEECH_CACHE)))
        _SPEECH_CACHE[cache_key] = result

    return result or (b"", "audio/mpeg")
