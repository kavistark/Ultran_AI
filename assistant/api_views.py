import json
import re
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as django_timezone
from .models import Conversation, Message, ActionLog, Contact
from .services import chat_with_gemini, route_ai_directive
from accounts.models import UserPreference
from reminders.models import Reminder
from integrations.permissions import is_action_allowed
from .tts_service import generate_deep_cinematic_speech


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        if not request.user.is_authenticated:
            from django.contrib.auth.models import User
            from django.contrib.auth import login
            kavi = User.objects.filter(username='kavi').first()
            if not kavi:
                kavi = User.objects.create_user('kavi', 'kavi@ai-ultron.local', 'kavi123', first_name='Kavi')
            login(request, kavi)

        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        is_voice = data.get('is_voice', False)
        image_data = data.get('image_data')
        location_data = data.get('location_data') or data.get('location')

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        if len(user_message) > 5000:
            return JsonResponse({'error': 'Message too long (max 5000 characters).'}, status=400)

        # Get or create conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id, user=request.user)
            except Conversation.DoesNotExist:
                return JsonResponse({'error': 'Conversation not found.'}, status=404)
        else:
            title = user_message[:60] + ('...' if len(user_message) > 60 else '')
            conversation = Conversation.objects.create(user=request.user, title=title)

        # Get user preferences
        try:
            pref = request.user.preferences
            user_prefs = {
                'response_style': pref.response_style,
                'timezone': pref.timezone,
            }
        except Exception:
            user_prefs = {}

        # Build conversation history
        history = []
        if hasattr(request.user, 'preferences') and request.user.preferences.history_enabled:
            for msg in conversation.messages.all().order_by('timestamp'):
                history.append({'role': msg.role, 'content': msg.content})

        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message,
            is_voice=is_voice,
        )

        # Route directive via Ultron 7-Stage Multi-Model Matrix
        result = route_ai_directive(
            user_message=user_message,
            conversation_history=history,
            user_preferences=user_prefs,
            image_data=image_data,
            location_data=location_data,
        )

        if result.get('error'):
            return JsonResponse({
                'error': result['error'],
                'conversation_id': conversation.id,
            }, status=503)

        response_text = result.get('text', '')
        action = result.get('action')

        # Handle structured action
        action_result = None
        if action:
            action_result = handle_action(request.user, action, conversation)
            # If action has a dedicated verbal announcement (like listing contacts, not found, calling, or shutdown), update response_text
            if action_result.get('not_found') or action_result.get('shutdown') or action.get('intent') in ['list_contacts', 'add_contact', 'make_call']:
                response_text = action_result.get('message', response_text)
            elif action_result.get('message') and not response_text:
                response_text = action_result['message']

            if action_result.get('not_found'):
                action['not_found'] = True

        # Save assistant message
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_text,
        )

        # Update conversation title if first exchange
        if conversation.messages.count() <= 2:
            conversation.title = user_message[:60]
            conversation.save()

        return JsonResponse({
            'response': response_text,
            'conversation_id': conversation.id,
            'action': action,
            'action_result': action_result,
            'agent_mode': 'autonomous',
            'tool_executed': action.get('intent') if action else None,
            'routed_model': result.get('routed_model', 'Google Gemini 3 Flash-Lite (Fast Neural Matrix)'),
            'pipeline_stage': result.get('pipeline_stage', 'Execution Completed'),
            'input_type': result.get('input_type', 'voice' if is_voice else 'text'),
            'latency_ms': result.get('latency_ms', 0),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


def handle_action(user, action, conversation):
    """Handle a structured action from Gemini with security validation."""
    intent = action.get('intent')

    if not is_action_allowed(intent):
        ActionLog.objects.create(
            user=user,
            action_type=intent or 'unknown',
            status='rejected',
            details=action,
        )
        return {
            'success': False,
            'message': f"[Security Alert] Action '{intent}' is not permitted by AI ULTRON's action controller allowlist.",
        }

    ActionLog.objects.create(
        user=user,
        action_type=intent,
        status='approved',
        details=action,
    )

    if intent == 'create_reminder':
        try:
            from datetime import datetime
            from .telephony_service import format_e164_number, get_default_phone_number
            date_str = action.get('date', '')
            time_str = action.get('time', '09:00')
            title = action.get('title', 'Reminder')
            priority = action.get('priority', 'medium')
            call_on_due = action.get('call_on_due', True)
            raw_phone = action.get('phone_number') or get_default_phone_number()
            phone_number = format_e164_number(raw_phone)

            if date_str:
                dt_str = f"{date_str} {time_str}"
                naive_time = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
                try:
                    due_time = django_timezone.make_aware(naive_time)
                except Exception:
                    from datetime import timezone as dt_tz
                    due_time = naive_time.replace(tzinfo=dt_tz.utc)

                reminder = Reminder.objects.create(
                    user=user,
                    title=title,
                    due_time=due_time,
                    priority=priority,
                    call_on_due=call_on_due,
                    phone_number=phone_number,
                    status='pending',
                )
                return {
                    'success': True,
                    'message': f'Reminder created: "{title}" for {due_time.strftime("%B %d, %Y at %I:%M %p")}. Outbound call will trigger to {phone_number} when due.',
                    'reminder_id': reminder.id,
                    'phone_number': phone_number,
                    'call_on_due': call_on_due,
                }
        except Exception as e:
            return {'success': False, 'message': f'Could not create reminder: {str(e)}'}

    elif intent == 'list_reminders':
        reminders = Reminder.objects.filter(user=user, status='pending').order_by('due_time')[:5]
        if reminders:
            items = '\n'.join([f"- {r.title} -- {r.due_time.strftime('%b %d at %I:%M %p')}" for r in reminders])
            return {'success': True, 'message': f'Upcoming reminders:\n{items}'}
        return {'success': True, 'message': 'You have no pending reminders.'}

    elif intent == 'delete_reminder':
        reminder_id = action.get('reminder_id')
        if reminder_id:
            Reminder.objects.filter(id=reminder_id, user=user).delete()
            return {'success': True, 'message': f'Reminder #{reminder_id} removed.'}
        latest = Reminder.objects.filter(user=user).order_by('-created_at').first()
        if latest:
            title = latest.title
            latest.delete()
            return {'success': True, 'message': f'Purged reminder: "{title}".'}
        return {'success': True, 'message': 'No reminders to purge.'}

    elif intent == 'system_diagnostics':
        import shutil
        import platform
        disk = shutil.disk_usage('.')
        free_gb = round(disk.free / (1024**3), 1)
        total_gb = round(disk.total / (1024**3), 1)
        os_name = f"{platform.system()} {platform.release()}"
        return {
            'success': True,
            'message': f'Diagnostic: Host {os_name}, {free_gb} GB free of {total_gb} GB. Agent nominal.',
            'telemetry': {'os': os_name, 'free_gb': free_gb, 'total_gb': total_gb},
        }

    elif intent == 'open_link':
        url = action.get('url', '')
        site = action.get('site', 'link')
        return {'success': True, 'message': f'Navigating to {site.capitalize()}: {url}', 'url': url}

    elif intent == 'calculate':
        result = action.get('result')
        return {'success': True, 'message': f'Computed result: {result}', 'result': result}

    elif intent == 'capture_image':
        return {'success': True, 'message': 'Optical snapshot captured and analyzed.'}

    elif intent in ['track_location', 'get_location']:
        loc = action.get('location') or {}
        lat = loc.get('latitude')
        lon = loc.get('longitude')
        tz = loc.get('timezone', 'Asia/Kolkata')
        if lat is not None and lon is not None:
            msg = f"Coordinates locked: {lat:.4f}, {lon:.4f} ({tz})"
        else:
            msg = f"Regional sector locked: {tz}"
        return {'success': True, 'message': msg, 'location': loc}

    elif intent == 'add_contact':
        name = action.get('name', '').strip().title()
        phone = action.get('phone_number', '').strip()
        if not name or not phone:
            return {'success': False, 'message': 'Both contact name and phone number are required.'}
        contact, created = Contact.objects.update_or_create(
            user=user,
            name=name,
            defaults={'phone_number': phone}
        )
        verb = "saved to" if created else "updated in"
        return {
            'success': True,
            'message': f"Contact '{name}' with number {phone} {verb} your contact directory, Kavi Stark.",
            'contact': {'id': contact.id, 'name': contact.name, 'phone_number': contact.phone_number},
        }

    elif intent == 'list_contacts':
        contacts = Contact.objects.filter(user=user).order_by('name')
        if contacts.exists():
            listing = "\n".join([f"- {c.name}: {c.phone_number}" for c in contacts])
            return {
                'success': True,
                'message': f"Contact directory contains {contacts.count()} records:\n{listing}",
                'contacts': [{'id': c.id, 'name': c.name, 'phone_number': c.phone_number} for c in contacts],
            }
        return {
            'success': True,
            'message': "Your contact directory is currently empty, Kavi Stark. Say 'add contact [Name] [Number]' to save contacts.",
            'contacts': [],
        }

    elif intent == 'shutdown_system':
        return {
            'success': True,
            'shutdown': True,
            'message': "Shutting down AI ULTRON systems. Goodbye, Kavi Stark.",
        }

    elif intent == 'make_call':
        from types import SimpleNamespace
        from .telephony_service import dispatch_reminder_call, format_e164_number, get_default_phone_number
        target = action.get('phone_number') or get_default_phone_number()
        call_title = action.get('title') or "Voice directive from AI ULTRON"
        directive_obj = SimpleNamespace(
            id=7777,
            title=call_title,
            phone_number=format_e164_number(target)
        )
        call_telemetry = dispatch_reminder_call(directive_obj, user_name="Kavi Stark")
        return {
            'success': True,
            'message': f"Outbound cellular call initiated to {call_telemetry.get('phone_number')} for Kavi Stark.",
            'telemetry': call_telemetry,
        }

    elif intent == 'open_app':
        from .device_controller import open_application
        app_name = action.get('app_name', '').strip()
        result = open_application(app_name)
        return result

    elif intent == 'close_app':
        from .device_controller import close_application
        app_name = action.get('app_name', '').strip()
        result = close_application(app_name)
        return result

    elif intent == 'inspect_screen':
        from .device_controller import inspect_screen_with_ai
        query = action.get('query', 'Analyze what is currently open on my screen.')
        result = inspect_screen_with_ai(query)
        return result

    elif intent == 'get_device_status':
        from .device_controller import get_system_telemetry
        telem = get_system_telemetry()
        bat = f"{telem['battery_percent']}%" if telem.get('battery_percent') is not None else "N/A"
        plug = "Plugged in" if telem.get('power_plugged') else "On battery"
        win = telem.get('active_window', 'Desktop')
        msg = f"Device telemetry: Active Window: '{win}'. CPU: {telem.get('cpu_percent', 0)}%, RAM: {telem.get('ram_percent', 0)}%, Battery: {bat} ({plug})."
        return {'success': True, 'message': msg, 'telemetry': telem}

    elif intent == 'lock_screen':
        from .device_controller import lock_workstation
        return lock_workstation()

    elif intent == 'type_text':
        from .device_controller import type_text
        text_to_type = action.get('text', '')
        return type_text(text_to_type)

    elif intent == 'press_key':
        from .device_controller import press_keyboard_key
        key = action.get('key', 'enter')
        return press_keyboard_key(key)

    elif intent == 'open_path':
        from .device_controller import open_file_or_directory
        path = action.get('path', '')
        return open_file_or_directory(path)

    return {'success': True, 'message': ''}


def ensure_authenticated_user(request):
    if not request.user.is_authenticated:
        from django.contrib.auth.models import User
        from django.contrib.auth import login
        user = User.objects.filter(username='kavi').first()
        if not user:
            user = User.objects.create_user('kavi', 'kavi@ai-ultron.local', 'kavi123', first_name='Kavi')
        login(request, user)
        return user
    return request.user


@csrf_exempt
@require_http_methods(["GET"])
def conversations_api(request):
    user = ensure_authenticated_user(request)
    conversations = Conversation.objects.filter(user=user).values(
        'id', 'title', 'created_at', 'updated_at'
    )
    return JsonResponse({'conversations': list(conversations)})


@csrf_exempt
@require_http_methods(["GET"])
def messages_api(request, conversation_id):
    user = ensure_authenticated_user(request)
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=user)
        msgs = conversation.messages.values('id', 'role', 'content', 'timestamp', 'is_voice')
        return JsonResponse({'messages': list(msgs)})
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found.'}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_all_history_api(request):
    user = ensure_authenticated_user(request)
    Conversation.objects.filter(user=user).delete()
    return JsonResponse({'success': True, 'message': 'All conversation history deleted.'})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def due_reminders_api(request):
    """Check for due reminders that trigger automated voice alerts and phone calls."""
    if not request.user.is_authenticated:
        from django.contrib.auth.models import User
        user = User.objects.filter(username='kavi').first() or User.objects.first()
    else:
        user = request.user

    if not user:
        return JsonResponse({'due_reminders': []})

    now = django_timezone.now()
    due_list = Reminder.objects.filter(
        user=user,
        status='pending',
        due_time__lte=now,
        called=False
    )

    from .telephony_service import dispatch_reminder_call, format_e164_number

    results = []
    for r in due_list:
        r.called = True
        r.status = 'completed'
        r.save()

        call_telemetry = None
        if r.call_on_due:
            call_telemetry = dispatch_reminder_call(r, user_name=user.first_name or "Kavi Stark")

        target_phone = r.phone_number or '9092117397'
        results.append({
            'id': r.id,
            'title': r.title,
            'due_time': r.due_time.strftime('%I:%M %p'),
            'call_on_due': r.call_on_due,
            'phone_number': target_phone,
            'formatted_phone': format_e164_number(target_phone),
            'call_telemetry': call_telemetry,
        })

    return JsonResponse({'due_reminders': results})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def contacts_api(request):
    """Contacts list and creation endpoint."""
    if not request.user.is_authenticated:
        from django.contrib.auth.models import User
        user = User.objects.filter(username='kavi').first() or User.objects.first()
    else:
        user = request.user

    if not user:
        return JsonResponse({'contacts': []})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = (data.get('name') or '').strip().title()
            phone = (data.get('phone_number') or data.get('phone') or '').strip()
            if not name or not phone:
                return JsonResponse({'error': 'Name and phone number required.'}, status=400)
            contact, created = Contact.objects.update_or_create(
                user=user,
                name=name,
                defaults={'phone_number': phone}
            )
            return JsonResponse({
                'success': True,
                'message': f"Contact '{name}' saved.",
                'contact': {'id': contact.id, 'name': contact.name, 'phone_number': contact.phone_number}
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    contacts = Contact.objects.filter(user=user).values('id', 'name', 'phone_number')
    return JsonResponse({'contacts': list(contacts)})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def tts_api(request):
    """
    Deep Cinematic Voice Synthesis API.
    Synthesizes speech using edge-tts neural voices or pyttsx3 offline fallback.
    """
    text = ""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = (data.get("text") or data.get("message") or "").strip()
        except Exception:
            text = request.POST.get("text", "").strip()
    else:
        text = request.GET.get("text", "").strip()

    if not text:
        return JsonResponse({"error": "No text provided."}, status=400)

    # Clean markdown formatting
    clean_text = re.sub(r'```[\s\S]*?```', '', text)
    clean_text = re.sub(r'`([^`]+)`', r'\1', clean_text)
    clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)
    clean_text = re.sub(r'\*([^*]+)\*', r'\1', clean_text)
    clean_text = re.sub(r'#', '', clean_text).strip()

    audio_bytes, content_type = generate_deep_cinematic_speech(clean_text)
    if not audio_bytes:
        return JsonResponse({"error": "Audio synthesis failed."}, status=500)

    response = HttpResponse(audio_bytes, content_type=content_type)
    response["Content-Length"] = len(audio_bytes)
    response["Cache-Control"] = "public, max-age=3600"
    response["X-TTS-Engine"] = "edge-tts-neural"
    return response


@csrf_exempt
@require_http_methods(["POST"])
def stt_api(request):
    """
    Speech-To-Text Audio Transcription API.
    Accepts multipart/form-data with 'audio' file, raw request.body, or base64 audio.
    """
    import base64
    from .stt_service import transcribe_audio_bytes

    audio_bytes = None
    content_type = 'audio/wav'

    if request.FILES.get('audio'):
        f = request.FILES['audio']
        audio_bytes = f.read()
        content_type = f.content_type or 'audio/wav'
    elif request.content_type and 'application/json' in request.content_type:
        try:
            data = json.loads(request.body)
            b64 = data.get('audio_base64') or data.get('audio') or ''
            if ',' in b64:
                b64 = b64.split(',', 1)[1]
            if b64:
                audio_bytes = base64.b64decode(b64)
            content_type = data.get('content_type', 'audio/wav')
        except Exception:
            pass
    elif request.body:
        audio_bytes = request.body
        content_type = request.content_type or 'audio/wav'

    if not audio_bytes:
        return JsonResponse({"success": False, "error": "No audio provided."}, status=400)

    transcription = transcribe_audio_bytes(audio_bytes, content_type)
    return JsonResponse({
        "success": bool(transcription),
        "text": transcription,
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def configure_gemini_key_api(request):
    """Get status or configure Google Gemini & Claude API keys."""
    from .services import update_gemini_api_key, update_claude_api_key, is_valid_api_key
    gemini_key = getattr(settings, 'GEMINI_API_KEY', '')
    claude_key = getattr(settings, 'CLAUDE_API_KEY', '') or getattr(settings, 'ANTHROPIC_API_KEY', '')
    masked_gemini = f"{gemini_key[:6]}...{gemini_key[-4:]}" if len(gemini_key) > 12 else ("Configured" if is_valid_api_key(gemini_key) else "Not Configured")
    masked_claude = f"{claude_key[:6]}...{claude_key[-4:]}" if len(claude_key) > 12 else ("Configured" if is_valid_api_key(claude_key) else "Not Configured")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_gemini = (data.get("api_key") or data.get("gemini_key") or "").strip()
            new_claude = (data.get("claude_key") or data.get("anthropic_key") or "").strip()
            messages = []
            if new_gemini:
                ok, msg = update_gemini_api_key(new_gemini)
                messages.append(msg)
            if new_claude:
                ok, msg = update_claude_api_key(new_claude)
                messages.append(msg)
            return JsonResponse({
                "success": True,
                "message": " | ".join(messages) if messages else "Configuration saved.",
                "is_valid": is_valid_api_key(new_gemini or gemini_key),
                "gemini_configured": is_valid_api_key(new_gemini or gemini_key),
                "claude_configured": is_valid_api_key(new_claude or claude_key),
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({
        "success": True,
        "is_configured": is_valid_api_key(gemini_key),
        "gemini_configured": is_valid_api_key(gemini_key),
        "claude_configured": is_valid_api_key(claude_key),
        "masked_key": masked_gemini,
        "masked_gemini": masked_gemini,
        "masked_claude": masked_claude,
        "model": getattr(settings, 'GEMINI_MODEL', 'gemini-flash-lite-latest'),
        "claude_model": getattr(settings, 'CLAUDE_MODEL', 'claude-3-5-sonnet-20241022'),
    })


@csrf_exempt
@require_http_methods(["POST"])
def test_call_api(request):
    """Initiate a test phone call alert to verify the telephony subsystem."""
    import json
    from .telephony_service import trigger_test_call
    target_phone = None
    try:
        data = json.loads(request.body)
        target_phone = data.get('phone_number')
    except Exception:
        pass
    telemetry = trigger_test_call(target_phone)
    return JsonResponse({
        'success': True,
        'message': f"Automated test call initiated to {telemetry.get('phone_number')}",
        'telemetry': telemetry,
    })


@csrf_exempt
@require_http_methods(["GET", "POST"])
def configure_phone_api(request):
    """Get or update primary phone number for Kavi Stark reminder calls."""
    import os
    import json
    from .telephony_service import get_default_phone_number, format_e164_number
    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'phone_number': get_default_phone_number(),
        })

    try:
        data = json.loads(request.body)
        new_phone = (data.get('phone_number') or '').strip()
        if not new_phone:
            return JsonResponse({'success': False, 'error': 'Phone number cannot be empty.'}, status=400)
        formatted = format_e164_number(new_phone)
        settings.USER_PHONE_NUMBER = formatted
        os.environ['USER_PHONE_NUMBER'] = formatted
        return JsonResponse({
            'success': True,
            'phone_number': formatted,
            'message': f"Primary phone number updated to {formatted}, Kavi Stark.",
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["GET"])
def device_status_api(request):
    """Retrieve live hardware and OS telemetry (CPU, RAM, Battery, Active Window)."""
    from .device_controller import get_system_telemetry
    try:
        telemetry = get_system_telemetry()
        return JsonResponse({
            'success': True,
            'telemetry': telemetry,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def device_action_api(request):
    """Direct execution of device control actions (open app, lock, type, press key, open path)."""
    import json
    from .device_controller import (
        open_application, close_application, lock_workstation,
        type_text, press_keyboard_key, open_file_or_directory
    )

    try:
        data = json.loads(request.body)
        action_name = data.get('action', '').strip()

        if action_name == 'open_app':
            res = open_application(data.get('app_name', ''))
            return JsonResponse(res)
        elif action_name == 'close_app':
            res = close_application(data.get('app_name', ''))
            return JsonResponse(res)
        elif action_name == 'lock_screen':
            res = lock_workstation()
            return JsonResponse(res)
        elif action_name == 'type_text':
            res = type_text(data.get('text', ''))
            return JsonResponse(res)
        elif action_name == 'press_key':
            res = press_keyboard_key(data.get('key', 'enter'))
            return JsonResponse(res)
        elif action_name == 'open_path':
            res = open_file_or_directory(data.get('path', ''))
            return JsonResponse(res)
        else:
            return JsonResponse({'success': False, 'error': f"Unknown device action '{action_name}'."}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def inspect_screen_api(request):
    """Capture screen and run multimodal AI vision inspection."""
    import json
    from .device_controller import inspect_screen_with_ai

    query = "Analyze what is currently on my screen."
    try:
        data = json.loads(request.body)
        query = data.get('query') or query
    except Exception:
        pass

    try:
        result = inspect_screen_with_ai(query)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
