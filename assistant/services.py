import json
import re
import os
from datetime import datetime, timedelta
from django.conf import settings
from .prompts import build_system_prompt, DOCUMENT_ANALYSIS_PROMPT

# Supported intents that ULTRAN can execute
SUPPORTED_INTENTS = {
    'create_reminder',
    'list_reminders',
    'delete_reminder',
    'create_task',
    'list_tasks',
    'summarize_document',
    'open_link',
    'general_chat',
}


def is_valid_api_key(key):
    return bool(key and key.strip() and key.strip() != 'your-gemini-api-key-here')


def get_gemini_client():
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not is_valid_api_key(api_key):
        raise ValueError("GEMINI_API_KEY is not configured. Please set your key in the .env file.")
    from google import genai
    from google.genai import types
    return genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=15000))


def extract_json_from_text(text):
    """Extract JSON block from Gemini response if present."""
    pattern = r'```json\s*([\s\S]*?)\s*```'
    match = re.search(pattern, text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    # Try raw JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    return None


def local_fallback_parser(user_message, conversation_history=None, user_preferences=None, timezone='UTC'):
    """
    Local rule-based fallback processor for offline or non-API environments.
    Extracts intents like reminders and answers common questions honestly.
    """
    msg_lower = user_message.lower().strip()

    # Check for unsupported hardware/phone actions
    if any(phrase in msg_lower for phrase in ['unlock my phone', 'unlock phone', 'open camera', 'turn on flashlight', 'read my sms']):
        return {
            'text': "I cannot perform hardware device operations directly through the web client.",
            'action': None,
            'error': None,
        }

    # Check for reminder intent
    if 'remind' in msg_lower or 'reminder' in msg_lower:
        # Check if user asks to list reminders
        if any(w in msg_lower for w in ['show', 'list', 'what are', 'view', 'check']):
            return {
                'text': "Here are your scheduled reminders from the database.",
                'action': {'intent': 'list_reminders'},
                'error': None,
            }

        title = "Scheduled Task"
        match = re.search(r'remind me to\s+(.*?)(?:\s+tomorrow|\s+today|\s+at|\s+on|$)', msg_lower)
        if match:
            title = match.group(1).strip().capitalize()
        elif 'remind me' in msg_lower:
            parts = msg_lower.split('remind me')
            if len(parts) > 1:
                title = parts[1].strip().capitalize()

        target_date = datetime.now()
        if 'tomorrow' in msg_lower:
            target_date += timedelta(days=1)
        elif 'next week' in msg_lower:
            target_date += timedelta(days=7)

        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', msg_lower)
        target_time = "09:00"
        if time_match:
            hr = int(time_match.group(1))
            mn = time_match.group(2) or "00"
            period = (time_match.group(3) or "").lower()
            if period == 'pm' and hr < 12:
                hr += 12
            elif period == 'am' and hr == 12:
                hr = 0
            target_time = f"{hr:02d}:{mn}"

        action = {
            'intent': 'create_reminder',
            'title': title,
            'date': target_date.strftime('%Y-%m-%d'),
            'time': target_time,
            'priority': 'medium',
            'requires_confirmation': True,
        }
        return {
            'text': f"I have set your reminder for {title} on {action['date']} at {action['time']}.",
            'action': action,
            'error': None,
        }

    # Questions about capabilities or greetings
    if any(w in msg_lower for w in ['hello', 'hi', 'hey', 'who are you', 'help me', 'what can you do']):
        return {
            'text': "Hello Kavi Stark, I am AI ULTRAN, your personal voice assistant. How can I assist you right now?",
            'action': None,
            'error': None,
        }

    # Sample explanation queries
    if 'python decorator' in msg_lower or 'decorator' in msg_lower:
        return {
            'text': "A Python decorator is a function that modifies or extends the behavior of another function without altering its source code.",
            'action': None,
            'error': None,
        }

    if 'machine learning' in msg_lower:
        return {
            'text': "Machine learning is a field of artificial intelligence where algorithms learn patterns from data to make predictions without explicit programming.",
            'action': None,
            'error': None,
        }

    if 'artificial intelligence' in msg_lower or 'what is ai' in msg_lower:
        return {
            'text': "Artificial intelligence is computer science focused on building intelligent systems capable of reasoning, problem solving, and language understanding.",
            'action': None,
            'error': None,
        }

    # Generic fallback when network is unavailable
    if any(w in msg_lower for w in ['explain', 'what is', 'what are', 'how does', 'why is', 'tell me about']):
        return {
            'text': "Network is currently busy. Please ask again in a moment.",
            'action': None,
            'error': None,
        }

    return {
        'text': "I am listening, Kavi Stark. How can I assist you?",
        'action': None,
        'error': None,
    }


def chat_with_gemini(user_message, conversation_history=None, user_preferences=None, timezone='UTC'):
    """
    Send a message to Gemini and return the response.
    Falls back gracefully to local rule-based intelligence when API key is missing or quota is reached.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')

    # Fast-path for restricted hardware operations (immediate response)
    msg_lower = user_message.lower().strip()
    if any(phrase in msg_lower for phrase in ['unlock my phone', 'unlock phone', 'open camera', 'turn on flashlight', 'flashlight', 'read my sms', 'send sms']):
        return local_fallback_parser(user_message, conversation_history=conversation_history, user_preferences=user_preferences, timezone=timezone)

    # If no valid API key is present, use local fallback parser
    if not is_valid_api_key(api_key):
        return local_fallback_parser(user_message, conversation_history=conversation_history, user_preferences=user_preferences, timezone=timezone)

    try:
        from google import genai
        from google.genai import types

        client = get_gemini_client()

        # Build system prompt
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response_style = 'concise'
        if user_preferences:
            response_style = user_preferences.get('response_style', 'concise')
            tz = user_preferences.get('timezone', 'UTC')
            if tz:
                timezone = tz

        system_prompt = build_system_prompt(
            response_style=response_style,
            timezone=timezone,
            current_datetime=current_datetime,
        )

        contents = []

        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:
                role = 'user' if msg.get('role') == 'user' else 'model'
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part(text=msg.get('content', ''))]
                ))

        # Add current user message
        contents.append(types.Content(
            role='user',
            parts=[types.Part(text=user_message)]
        ))

        model_pref = getattr(settings, 'GEMINI_MODEL', 'gemini-3.5-flash-lite')
        candidate_models = []
        for m in [model_pref, 'gemini-3.5-flash-lite', 'gemini-3.5-flash']:
            if m and m not in candidate_models:
                candidate_models.append(m)

        response = None
        last_error = None
        for m_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                        max_output_tokens=2048,
                    )
                )
                if response and response.text:
                    break
            except Exception as ex:
                last_error = ex
                continue

        if not response:
            raise last_error or Exception("No response generated from Gemini models.")

        response_text = response.text or ''

        # Check for structured action in response
        action = extract_json_from_text(response_text)
        if action and action.get('intent') in SUPPORTED_INTENTS:
            clean_text = re.sub(r'```json\s*[\s\S]*?\s*```', '', response_text).strip()
            if not clean_text:
                clean_text = f"I'll help you with that. Processing {action.get('intent', 'request').replace('_', ' ')}."
            return {
                'text': clean_text,
                'action': action,
                'error': None,
            }

        return {
            'text': response_text,
            'action': None,
            'error': None,
        }

    except Exception as e:
        import logging
        logging.getLogger(__name__).warning("Gemini API call notice: %s", str(e))
        # Fallback cleanly to local intelligence without polluting voice output with error text
        fallback = local_fallback_parser(
            user_message,
            conversation_history=conversation_history,
            user_preferences=user_preferences,
            timezone=timezone
        )
        return fallback


def analyze_document_with_gemini(document_content, document_name, user_question):
    """Analyze a document and answer user question about it."""
    api_key = getattr(settings, 'GEMINI_API_KEY', '')

    if not is_valid_api_key(api_key):
        # Local document summarizer fallback
        lines = [line.strip() for line in document_content.splitlines() if line.strip()]
        total_words = sum(len(line.split()) for line in lines)
        sample = '\n'.join(lines[:10])

        summary = (
            f"### Document Analysis: {document_name}\n\n"
            f"**File Overview**:\n"
            f"• Estimated word count: ~{total_words} words\n"
            f"• Total content lines: {len(lines)}\n\n"
            f"**Preview of Content**:\n"
            f"{sample}\n\n"
            f"*(Connect a live GEMINI_API_KEY in `.env` to enable semantic vector questions and full deep reasoning)*"
        )
        return {'text': summary, 'error': None}

    try:
        from google import genai
        from google.genai import types

        client = get_gemini_client()

        prompt = DOCUMENT_ANALYSIS_PROMPT.format(
            document_name=document_name,
            document_content=document_content[:8000],
            user_question=user_question,
        )

        candidate_models = [
            getattr(settings, 'GEMINI_MODEL', 'gemini-flash-latest'),
            'gemini-flash-latest',
            'gemini-2.5-flash-lite',
        ]
        response = None
        for m_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                        max_output_tokens=2048,
                    )
                )
                if response and response.text:
                    break
            except Exception:
                continue

        if not response:
            raise Exception("Document analysis failed across available Gemini models.")

        return {'text': response.text, 'error': None}

    except Exception as e:
        return {'text': '', 'error': str(e)}
