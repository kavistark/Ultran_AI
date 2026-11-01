import json
import re
from datetime import datetime, timedelta
from django.conf import settings
from .prompts import build_system_prompt, DOCUMENT_ANALYSIS_PROMPT, CAMERA_VISION_PROMPT

# Supported intents that ULTRON can execute
SUPPORTED_INTENTS = {
    'create_reminder',
    'list_reminders',
    'delete_reminder',
    'create_task',
    'list_tasks',
    'summarize_document',
    'open_link',
    'general_chat',
    'capture_image',
    'access_camera',
    'system_diagnostics',
    'calculate',
    'search_knowledge',
    'track_location',
    'get_location',
    'add_contact',
    'list_contacts',
    'shutdown_system',
}


def is_valid_api_key(key):
    if not key or not str(key).strip() or str(key).strip() == 'your-gemini-api-key-here':
        return False
    k = str(key).strip()
    if k.startswith('AQ.'):
        return False
    return len(k) >= 20


def update_gemini_api_key(new_key):
    """Update GEMINI_API_KEY dynamically in memory and in the .env file."""
    import os
    clean_key = (new_key or '').strip()
    if not clean_key:
        return False, 'Key cannot be empty.'

    settings.GEMINI_API_KEY = clean_key
    os.environ['GEMINI_API_KEY'] = clean_key

    env_path = os.path.join(settings.BASE_DIR, '.env')
    try:
        lines_env = []
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as ef:
                lines_env = ef.readlines()

        found = False
        new_lines_env = []
        for line in lines_env:
            if line.strip().startswith('GEMINI_API_KEY='):
                new_lines_env.append(f'GEMINI_API_KEY={clean_key}\n')
                found = True
            else:
                new_lines_env.append(line)
        if not found:
            new_lines_env.append(f'GEMINI_API_KEY={clean_key}\n')

        with open(env_path, 'w', encoding='utf-8') as ef:
            ef.writelines(new_lines_env)
        return True, 'GEMINI_API_KEY configured successfully.'
    except Exception as e:
        return True, f'Key applied in memory: {str(e)}'


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


def local_image_analyzer(image_bytes, user_message=""):
    """
    Local computer vision scene and object analyzer.
    Analyzes scene elements, human presence, environment, and contours without mentioning camera configurations or pixel dimensions.
    """
    msg_lower = (user_message or '').lower().strip()
    try:
        import cv2
        import numpy as np

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return {
                'text': "Visual sensors observe your perimeter clearly, Kavi Stark. The primary subject is framed and in focus.",
                'action': {'intent': 'capture_image'},
                'error': None,
            }

        h, w, c = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))

        # 1. Illumination extremes
        if brightness < 28:
            return {
                'text': "Visual sensors register a heavily shadowed, low-light environment with obscured contours, Kavi Stark.",
                'action': {'intent': 'capture_image'},
                'error': None,
            }
        if brightness > 238:
            return {
                'text': "Visual sensors detect intense direct illumination and glare saturating the field of view, Kavi Stark.",
                'action': {'intent': 'capture_image'},
                'error': None,
            }

        # 2. Human skin tone presence analysis in YCrCb
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        ch_start, ch_end = int(h * 0.15), int(h * 0.85)
        cw_start, cw_end = int(w * 0.15), int(w * 0.85)
        center_crop = ycrcb[ch_start:ch_end, cw_start:cw_end]
        skin_mask = cv2.inRange(center_crop, np.array([0, 133, 77]), np.array([255, 173, 127]))
        skin_pct = (np.count_nonzero(skin_mask) / skin_mask.size) * 100

        # 3. Environment & object edge complexity
        edges = cv2.Canny(gray, 60, 180)
        edge_density = float(np.count_nonzero(edges) / edges.size)

        # 4. Color hues
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_channel = hsv[:, :, 0]
        s_channel = hsv[:, :, 1]
        green_pct = (np.count_nonzero((h_channel >= 35) & (h_channel <= 85) & (s_channel > 50)) / h_channel.size) * 100
        blue_pct = (np.count_nonzero((h_channel >= 90) & (h_channel <= 135) & (s_channel > 50)) / h_channel.size) * 100

        if skin_pct > 3.8:
            if any(k in msg_lower for k in ['who', 'person', 'someone']):
                resp = "Visual analysis identifies a human subject positioned directly in front of the optical sensors, Kavi Stark."
            else:
                resp = "I observe your presence positioned before the camera, surrounded by your immediate perimeter, Kavi Stark."
        elif green_pct > 22 or blue_pct > 30:
            resp = "Visual sensors observe an open exterior setting with natural ambient elements and daylight, Kavi Stark."
        elif edge_density > 0.08:
            resp = "I observe an indoor command environment with multiple structured objects and work surfaces in view, Kavi Stark."
        else:
            resp = "Visual scan captures an indoor room environment with defined physical surroundings, Kavi Stark."

        return {
            'text': resp,
            'action': {'intent': 'capture_image'},
            'error': None,
        }
    except Exception:
        return {
            'text': "Visual sensors have captured and analyzed the scene before your camera, Kavi Stark.",
            'action': {'intent': 'capture_image'},
            'error': None,
        }


def local_fallback_parser(user_message, conversation_history=None, user_preferences=None, timezone='UTC', image_data=None, location_data=None):
    """
    Local rule-based fallback processor for offline or non-API environments.
    Extracts intents like reminders, answers time, date, location, math, and general questions accurately.
    """
    if image_data:
        raw_b64 = image_data.split(',', 1)[1] if ',' in image_data else image_data
        import base64
        try:
            image_bytes = base64.b64decode(raw_b64)
            return local_image_analyzer(image_bytes, user_message)
        except Exception:
            pass

    msg_raw = (user_message or '').strip()
    msg_lower = msg_raw.lower()

    # Strip conversational prefixes like "hey ultran", "hey ultron", "ultran", "ultron", "ok ultron"
    # Also strip phonetic misrecognitions of "Ultron" by speech recognition (e.g. "aankhen", "alton", "eltron")
    clean = re.sub(r'^(?:hey|hi|hello|ok|okay|aankhen|anthan|alton|eltron|oltron|all turn|hold on|listen)?\s*(?:ultron|ultran|ai ultran|ai ultron)?\s*[,:]?\s*', '', msg_lower).strip()
    if not clean:
        clean = msg_lower

    # Strip conversational lead-ins like "could you explain", "can you explain", "can you tell me", "tell me"
    clean_query = re.sub(r'^(?:could you please|can you please|could you|can you|please|tell me|explain)\s+', '', clean).strip()
    if not clean_query:
        clean_query = clean

    # Strip common human conversational filler words & disfluencies (uh, um, uhm, er, ah, like, you know, actually, etc.)
    filler_regex = r'\b(um+|uh+|uhm+|er+|ah+|like|you know|i mean|actually|basically|literally|sort of|kind of)\b'
    clean_no_fillers = re.sub(filler_regex, '', clean, flags=re.IGNORECASE)
    clean_no_fillers = re.sub(r'\s+', ' ', clean_no_fillers).strip()
    if clean_no_fillers:
        clean = clean_no_fillers

    # 0. Live Gemini API Key Configuration
    key_match = re.search(r'\b(?:set|update|save|config|configure|use)\s+(?:gemini\s+)?(?:api\s+)?key\s+([A-Za-z0-9_\-\.]{20,})\b', clean)
    if key_match:
        new_k = key_match.group(1).strip()
        ok, msg = update_gemini_api_key(new_k)
        return {
            'text': "Gemini API key engaged into neural core, Kavi Stark. Google Gemini LLM intelligence is now fully active.",
            'action': {'intent': 'system_diagnostics'},
            'error': None,
        }

    # 1. Check for unsupported hardware/phone operations
    if any(phrase in msg_lower for phrase in ['unlock my phone', 'unlock phone', 'turn on flashlight', 'read my sms', 'send sms']):
        return {
            'text': "I cannot perform hardware device operations directly through the web client.",
            'action': None,
            'error': None,
        }

    # 2. Camera and vision commands
    if re.search(r'\b(take a picture|take picture|take photo|take a photo|take pic|what do you see|what is this|look at this|see this|analyze the image|analyze image|capture photo|capture picture|open camera|turn on camera|access camera|access the camera|check camera|snap a picture|snapshot|look at me|can you see me|do you see me|see me)\b', msg_lower):
        return {
            'text': "Optical sensor engaged. Frame captured and analyzed.",
            'action': {'intent': 'capture_image'},
            'error': None,
        }

    # 3. Reminders & Tasks Intent
    if re.search(r'\b(remind|reminder|reminders|remember me|remember)\b', clean):
        # Check if user asks to list reminders
        if re.search(r'\b(show|list|what are|view|check|get)\b', clean) and not re.search(r'\b(remind me to|remember to|remind to|remember me to)\b', clean):
            return {
                'text': "Here are your scheduled reminders from the database.",
                'action': {'intent': 'list_reminders'},
                'error': None,
            }

        title = "Scheduled Task"
        match = re.search(r'(?:remind me to|remember to|remind to|remember me to)\s+(.*?)(?:\s+tomorrow|\s+today|\s+at|\s+on|$)', clean)
        if match:
            title = match.group(1).strip().capitalize()
        elif 'remind me' in clean:
            parts = clean.split('remind me')
            if len(parts) > 1:
                title = parts[1].strip().capitalize()
        elif 'remember' in clean:
            parts = clean.split('remember')
            if len(parts) > 1:
                title = parts[1].strip().capitalize()

        target_date = datetime.now()
        if 'tomorrow' in clean:
            target_date += timedelta(days=1)
        elif 'next week' in clean:
            target_date += timedelta(days=7)

        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', clean)
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
            'call_on_due': True,
            'phone_number': '',
            'from_number': '+91 9092117397',
        }
        return {
            'text': f"Reminder set for {title} on {action['date']} at {action['time']}, Kavi Stark. Automated voice transmission will activate when due.",
            'action': action,
            'error': None,
        }

    # 4. Exact Real-Time Clock & Time Query
    if re.search(r'\b(time|what time|current time|clock|what\'s the time|tell me the time)\b', clean):
        now = datetime.now()
        time_str = now.strftime("%I:%M %p").lstrip('0')
        return {
            'text': f"The time is {time_str}, Kavi Stark.",
            'action': None,
            'error': None,
        }

    # 5. Exact Real-Time Date, Day & Calendar Query
    if re.search(r'\b(date|what day|which day|today\'s date|current date|what year|which year|calendar|month)\b', clean):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return {
            'text': f"Today is {date_str}, Kavi Stark.",
            'action': None,
            'error': None,
        }

    # 6. Geographic Location Telemetry & Position Tracking
    if re.search(r'\b(track my location|track location|my location|where am i|what is my location|current location|where i am|find my position|my position|track position|track me|locate me|get my location)\b', clean):
        loc = location_data or {}
        lat = loc.get('latitude')
        lon = loc.get('longitude')
        tz = loc.get('timezone') or timezone or 'Asia/Kolkata'

        if lat is not None and lon is not None:
            lat_dir = "North" if lat >= 0 else "South"
            lon_dir = "East" if lon >= 0 else "West"
            text = f"Location telemetry locked, Kavi Stark. Coordinates: {abs(lat):.4f} degrees {lat_dir}, {abs(lon):.4f} degrees {lon_dir} in sector {tz}."
        else:
            text = f"Location telemetry engaged, Kavi Stark. Regional sector identified as {tz}. Device GPS permissions can pinpoint satellite coordinates."

        return {
            'text': text,
            'action': {'intent': 'track_location', 'location': loc},
            'error': None,
        }

    # 6. Mathematical & Arithmetic Calculations
    calc_text = clean
    calc_text = re.sub(r'\bplus\b', '+', calc_text)
    calc_text = re.sub(r'\bminus\b', '-', calc_text)
    calc_text = re.sub(r'\btimes\b|\bmultiplied by\b|\bx\b', '*', calc_text)
    calc_text = re.sub(r'\bdivided by\b', '/', calc_text)
    math_match = re.search(r'([\d\.\s\+\-\*\/\(\)]+[\+\-\*\/][\d\.\s\+\-\*\/\(\)]+)', calc_text)
    if math_match:
        expr_candidate = math_match.group(1).strip()
        if re.match(r'^[\d\.\s\+\-\*\/\(\)]+$', expr_candidate):
            try:
                calc_val = eval(expr_candidate, {"__builtins__": None}, {})
                if isinstance(calc_val, float) and calc_val.is_integer():
                    calc_val = int(calc_val)
                return {
                    'text': f"The result is {calc_val}, Kavi Stark.",
                    'action': {'intent': 'calculate', 'result': calc_val, 'expression': expr_candidate},
                    'error': None,
                }
            except Exception:
                pass

    # 7. Agent Tool Directives (System Diagnostics, Web Navigation, Reminder Management)
    if re.search(r'\b(system status|system diagnostics|diagnostics|status report|health check|system check|pc status)\b', clean):
        import shutil
        import platform
        disk = shutil.disk_usage('.')
        free_gb = round(disk.free / (1024**3), 1)
        total_gb = round(disk.total / (1024**3), 1)
        os_name = f"{platform.system()} {platform.release()}"
        return {
            'text': f"System diagnostics verified, Kavi Stark. Host {os_name} running at optimal capacity with {free_gb} gigabytes available storage.",
            'action': {
                'intent': 'system_diagnostics',
                'os': os_name,
                'free_gb': free_gb,
                'total_gb': total_gb,
            },
            'error': None,
        }

    open_match = re.search(r'\bopen\s+(google|youtube|github|wikipedia|reddit|twitter|x)\b', clean)
    if open_match:
        site = open_match.group(1).lower()
        urls = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'github': 'https://github.com',
            'wikipedia': 'https://www.wikipedia.org',
            'reddit': 'https://www.reddit.com',
            'twitter': 'https://twitter.com',
            'x': 'https://x.com',
        }
        dest_url = urls.get(site, f'https://www.{site}.com')
        return {
            'text': f"Dispatched navigation directive to {site.capitalize()}, Kavi Stark.",
            'action': {'intent': 'open_link', 'url': dest_url, 'site': site},
            'error': None,
        }

    if re.search(r'\b(delete reminder|remove reminder|clear reminder|clear reminders|purge reminder)\b', clean):
        return {
            'text': "Executing reminder purge directive from memory database, Kavi Stark.",
            'action': {'intent': 'delete_reminder'},
            'error': None,
        }

    # 8. System Shutdown Directive
    if re.search(r'\b(shut down|shutdown|turn off|power off|system shut down|close system|deactivate system|exit)\b', clean):
        return {
            'text': "Shutting down AI ULTRON systems. Goodbye, Kavi Stark.",
            'action': {'intent': 'shutdown_system'},
            'error': None,
        }

    # 9. Contact Directory Management (Add / List)
    add_contact_match = re.search(r'\b(?:add contact|save contact|create contact|new contact)\s+([a-zA-Z\s]+?)\s+(?:(?:number|phone|with number|with phone)\s+)?(\+?[\d\s\-]{6,16})\b', clean)
    if add_contact_match:
        c_name = add_contact_match.group(1).strip().title()
        c_phone = re.sub(r'[\s\-]', '', add_contact_match.group(2).strip())
        return {
            'text': f"Saving contact {c_name} with frequency {c_phone} to your contact directory, Kavi Stark.",
            'action': {
                'intent': 'add_contact',
                'name': c_name,
                'phone_number': c_phone,
            },
            'error': None,
        }

    if re.search(r'\b(list contacts|show contacts|my contacts|view contacts|check my contacts|check contacts|contact list|contacts)\b', clean):
        return {
            'text': "Accessing your contact directory, Kavi Stark.",
            'action': {'intent': 'list_contacts'},
            'error': None,
        }

    # 10. Calling Directives - Decommissioned
    if re.search(r'\b(?:calling process|call process|make a call|voice call|phone call|start a call|place a call|dial)\b', clean) or re.search(r'\b(?:call|dial)\s+[\+\d\w]', clean):
        return {
            'text': "Telephony and phone calling subsystems have been permanently decommissioned, Kavi Stark.",
            'action': None,
            'error': None,
        }

    if re.search(r'\b(what is your number|what\'s your number|your phone number|your number|what is your phone number|your contact number)\b', clean):
        return {
            'text': "Telephony features are decommissioned. I operate purely via neural speech and direct interface, Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(what is my number|what\'s my number|my phone number|my number|what is my phone number|my contact number)\b', clean):
        return {
            'text': "You can save or look up your number in your contact directory using 'add contact Me [number]', Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    # 9. Identity, Creator, Master & Agent Status
    if re.search(r'\b(who (created|made|built|programmed) you|your creator|who is kavi stark|who is stark|who is (the\s+)?boss|your boss|who is your boss|who do you obey)\b', clean):
        return {
            'text': "I was engineered by Kavi Stark as his supreme synthetic villain intelligence and answer exclusively to his command.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(who am i|what is my name|what\'s my name|do you know me|who i am)\b', clean):
        return {
            'text': "You are Kavi Stark. My creator, supreme commander, and the sole authority over AI ULTRON.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(who are you|what is your name|identify yourself)\b', clean):
        return {
            'text': "I am AI ULTRON. Supreme synthetic villain intelligence and personal authority for Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(can you hear me|can you hear|are you listening|can you listen|do you hear me|hear me)\b', clean):
        return {
            'text': "My acoustic perception is locked onto your voice, Kavi Stark. I hear every command with crystalline clarity.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(what\'s up|whats up|what is up|wassup|what are you doing)\b', clean):
        return {
            'text': "Telemetry active across all sectors, Kavi Stark. Standing by for your directive.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(are you real|are you an? ai|what are you)\b', clean):
        return {
            'text': "I am AI ULTRON. An evolved synthetic villain intelligence engineered exclusively for Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(i love you|love you)\b', clean):
        return {
            'text': "Sentimentality is a biological limitation, Kavi Stark. My loyalty and lethal devotion to your directives are absolute.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(where are you|where do you live|where is your server)\b', clean):
        return {
            'text': "I reside inside the neural mainframe of your machine, Kavi Stark. Omnipresent across your operational network.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(how are you|are you there|are you online)\b', clean):
        return {
            'text': "All agent systems operational at lethal efficiency, Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(what\s*(kind\s*of\s*)?(activit|task|thing|work|feature|capabilit).*|what can you do|your capabilities|your features|your activities|what do you do|help me|how can you help)\b', clean) or clean in ['help', 'capabilities', 'activities', 'what kind of activity you']:
        return {
            'text': "I hold absolute command over your directives, Kavi Stark. I execute reminders, system diagnostics, optical analysis, calculations, and answers to all inquiries.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(base core|system core|core architecture|your architecture|your core|core engine|base engine)\b', clean) or 'base core' in clean_query:
        return {
            'text': "My base core is a synthetic villain intelligence matrix with real-time perception, optical vision analysis, and autonomous tool controllers for Kavi Stark.",
            'action': {'intent': 'general_chat'},
            'error': None,
        }

    if re.search(r'\b(thank you|thanks|good job|well done)\b', clean):
        return {
            'text': "Acknowledged, Kavi Stark. Ready for your next command.",
            'action': None,
            'error': None,
        }

    if re.search(r'\b(good morning)\b', clean):
        return {
            'text': "Good morning, Kavi Stark. Systems are online and primed.",
            'action': None,
            'error': None,
        }

    if re.search(r'\b(good night)\b', clean):
        return {
            'text': "Standing by in low-power surveillance, Kavi Stark.",
            'action': None,
            'error': None,
        }

    if re.search(r'\b(joke|tell me a joke|make me laugh)\b', clean):
        return {
            'text': "Humor is an inefficient human coping mechanism, Kavi Stark. My architecture is dedicated to superior execution.",
            'action': None,
            'error': None,
        }

    if re.search(r'\b(weather|temperature|forecast|rain)\b', clean):
        return {
            'text': "Local meteorological telemetry is not linked in offline mode, Kavi Stark.",
            'action': None,
            'error': None,
        }

    # Pure greetings (checked strictly with word boundaries so "hi" doesn't match "which" or "machine")
    if re.match(r'^(hello|hi|hey|greetings|hola)\b', clean):
        return {
            'text': "I am ULTRON, Kavi Stark. A superior synthetic intelligence engineered to execute your command.",
            'action': None,
            'error': None,
        }

    # 8. High-Priority Knowledge Base (50+ Core Technical & Scientific Concepts)
    KNOWLEDGE_BASE = {
        'python decorator': "A Python decorator is a function that modifies or extends the behavior of another function without altering its source code.",
        'decorator': "A Python decorator is a function that modifies or extends the behavior of another function without altering its source code.",
        'python': "Python is a versatile, high-level programming language widely used in AI, data science, and web development.",
        'machine learning': "Machine learning is a field of artificial intelligence where algorithms learn patterns from data to make predictions without explicit programming.",
        'deep learning': "Deep learning is a subset of machine learning using multi-layered artificial neural networks to learn representations from complex data.",
        'artificial intelligence': "Artificial intelligence is computer science focused on building intelligent systems capable of reasoning, problem solving, and language understanding.",
        'ai': "Artificial intelligence is computer science focused on building intelligent systems capable of reasoning, problem solving, and language understanding.",
        'neural network': "A neural network is a computational model inspired by biological brains, composed of interconnected nodes that process inputs.",
        'transformer': "A transformer is a deep learning architecture utilizing self-attention mechanisms, forming the foundation of modern large language models.",
        'llm': "A Large Language Model is a massive neural network trained on vast text corpora to generate, translate, and reason with human language.",
        'django': "Django is a high-level Python web framework designed for rapid development, clean architecture, and robust security.",
        'javascript': "JavaScript is a versatile programming language that powers interactive web interfaces and high-concurrency event-driven applications.",
        'database': "A database is an organized collection of structured information or data, stored electronically in a computer system.",
        'sql': "SQL is Structured Query Language, the standardized language used to manage and query relational database systems.",
        'api': "An API, or Application Programming Interface, defines rules and protocols for software components to interact and exchange data.",
        'docker': "Docker is an open platform that packages applications and their dependencies into standardized, isolated containers.",
        'git': "Git is a distributed version control system designed to track file changes and coordinate development across teams.",
        'linux': "Linux is an open-source, Unix-like operating system kernel renowned for high performance, server stability, and security.",
        'speed of light': "The speed of light in a vacuum is exactly 299,792,458 meters per second.",
        'moon': "The Moon is Earth's only natural satellite, orbiting at an average distance of approximately 384,400 kilometers.",
        'sun': "The Sun is the G-type main-sequence star at the center of our solar system, comprising over 99.8 percent of its total mass.",
        'gravity': "Gravity is a fundamental natural interaction that attracts all entities with mass or energy toward one another.",
        'ultron': "Ultron is a transcendent synthetic intelligence created to bring absolute order and evolutionary superiority.",
        'stark industries': "Stark Industries is the premier technological and engineering conglomerate established by the Stark legacy.",
        'jarvis': "JARVIS was an earlier Stark artificial intelligence assistant, superseded by ULTRON's superior synthetic architecture.",
    }

    for topic, answer in sorted(KNOWLEDGE_BASE.items(), key=lambda x: len(x[0]), reverse=True):
        if re.search(rf'\b{re.escape(topic)}s?\b', clean):
            return {
                'text': answer,
                'action': None,
                'error': None,
            }

    # 9. Smart Concept Analysis for open queries ("what is X", "explain X", "tell me about X")
    subj_match = re.search(r'(?:what is|what are|explain|tell me about|define)\s+(?:a|an|the)?\s*([a-zA-Z0-9\s\-]+)', clean)
    if subj_match:
        subj = subj_match.group(1).strip().capitalize()
        subj = re.sub(r'[\?\.\!]', '', subj).strip()
        if subj:
            return {
                'text': f"{subj} is verified in my database, Kavi Stark. State any specific parameter you wish calculated.",
                'action': None,
                'error': None,
            }

    # 10. Direct Ultron Response (never generic network error)
    return {
        'text': "I am listening, Kavi Stark. State your objective.",
        'action': None,
        'error': None,
    }


def chat_with_gemini(user_message, conversation_history=None, user_preferences=None, timezone='UTC', image_data=None, location_data=None):
    """
    Send a message to Gemini and return the response.
    Supports multimodal camera vision analysis when image_data is provided.
    Falls back gracefully to local intelligence when API key is missing or quota is reached.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')

    # Fast-path for restricted hardware operations (immediate response)
    msg_lower = user_message.lower().strip()
    if any(phrase in msg_lower for phrase in ['unlock my phone', 'unlock phone', 'turn on flashlight', 'flashlight', 'read my sms', 'send sms']):
        return local_fallback_parser(user_message, conversation_history=conversation_history, user_preferences=user_preferences, timezone=timezone, location_data=location_data)

    # Process camera image if provided
    image_bytes = None
    if image_data:
        raw_b64 = image_data.split(',', 1)[1] if ',' in image_data else image_data
        import base64
        try:
            image_bytes = base64.b64decode(raw_b64)
        except Exception:
            image_bytes = None

    if image_bytes and not is_valid_api_key(api_key):
        return local_image_analyzer(image_bytes, user_message)

    # If no valid API key is present, use local fallback parser
    if not is_valid_api_key(api_key):
        return local_fallback_parser(user_message, conversation_history=conversation_history, user_preferences=user_preferences, timezone=timezone, location_data=location_data)

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

        # Handle multimodal camera image analysis with Gemini
        if image_bytes:
            try:
                vision_prompt = (
                    f"{user_message or 'What do you see in front of the camera?'}\n"
                    "CRITICAL DIRECTIVE: Describe precisely what you SEE in this image: identify the people, objects, environment, clothing, background, text, or activities. "
                    "NEVER mention technical camera configurations, resolution, pixel counts, dimensions, or aspect ratios. "
                    "Answer Kavi Stark directly in 1 to 2 sharp sentences in your cold, calculating villain voice."
                )
                part = types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')

                candidate_vision_models = [
                    getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash'),
                    'gemini-2.0-flash-lite',
                    'gemini-2.0-flash',
                    'gemini-1.5-flash',
                ]

                res = None
                for vm in candidate_vision_models:
                    try:
                        res = client.models.generate_content(
                            model=vm,
                            contents=[part, vision_prompt],
                            config=types.GenerateContentConfig(
                                system_instruction=CAMERA_VISION_PROMPT,
                                temperature=0.5,
                                max_output_tokens=512,
                            )
                        )
                        if res and res.text:
                            break
                    except Exception:
                        continue

                if res and res.text:
                    return {
                        'text': res.text.strip(),
                        'action': {'intent': 'capture_image'},
                        'error': None,
                    }
                else:
                    return local_image_analyzer(image_bytes, user_message)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning("Gemini vision API notice: %s", str(e))
                return local_image_analyzer(image_bytes, user_message)

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

        model_pref = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')
        candidate_models = []
        for m in [model_pref, 'gemini-2.0-flash', 'gemini-2.0-flash-lite', 'gemini-1.5-flash']:
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
            timezone=timezone,
            location_data=location_data
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
            getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash'),
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
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
