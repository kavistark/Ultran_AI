import json
import re
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as django_timezone
from .models import Conversation, Message, ActionLog, Contact
from .services import chat_with_gemini
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

        # Call Gemini
        result = chat_with_gemini(
            user_message=user_message,
            conversation_history=history,
            user_preferences=user_prefs,
            image_data=image_data,
            location_data=location_data,
        )

        if result['error']:
            return JsonResponse({
                'error': result['error'],
                'conversation_id': conversation.id,
            }, status=503)

        response_text = result['text']
        action = result.get('action')

        # Handle structured action
        action_result = None
        if action:
            action_result = handle_action(request.user, action, conversation)
            # If action has a dedicated verbal announcement (like listing contacts, not found, or shutdown), update response_text
            if action_result.get('not_found') or action_result.get('shutdown') or action.get('intent') in ['list_contacts', 'add_contact']:
                response_text = action_result['message']
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
            'message': f"⚠️ Security Notice: Action '{intent}' is not permitted by AI ULTRON's action controller allowlist.",
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
            date_str = action.get('date', '')
            time_str = action.get('time', '09:00')
            title = action.get('title', 'Reminder')
            priority = action.get('priority', 'medium')

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
                    status='pending',
                )
                return {
                    'success': True,
                    'message': f'✅ Reminder created: "{title}" for {due_time.strftime("%B %d, %Y at %I:%M %p")}.',
                    'reminder_id': reminder.id,
                }
        except Exception as e:
            return {'success': False, 'message': f'Could not create reminder: {str(e)}'}

    elif intent == 'list_reminders':
        reminders = Reminder.objects.filter(user=user, status='pending').order_by('due_time')[:5]
        if reminders:
            items = '\n'.join([f"• {r.title} — {r.due_time.strftime('%b %d at %I:%M %p')}" for r in reminders])
            return {'success': True, 'message': f'📋 Your upcoming reminders:\n{items}'}
        return {'success': True, 'message': '📋 You have no pending reminders.'}

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
            listing = "\n".join([f"• {c.name}: {c.phone_number}" for c in contacts])
            return {
                'success': True,
                'message': f"📋 Contact directory contains {contacts.count()} records:\n{listing}",
                'contacts': [{'id': c.id, 'name': c.name, 'phone_number': c.phone_number} for c in contacts],
            }
        return {
            'success': True,
            'message': "📋 Your contact directory is currently empty, Kavi Stark. Say 'add contact [Name] [Number]' to save contacts.",
            'contacts': [],
        }

    elif intent == 'shutdown_system':
        return {
            'success': True,
            'shutdown': True,
            'message': "Shutting down AI ULTRON systems. Goodbye, Kavi Stark.",
        }

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
    """Check for due reminders that trigger automated voice alerts."""
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

    results = []
    for r in due_list:
        r.called = True
        r.status = 'completed'
        r.save()
        results.append({
            'id': r.id,
            'title': r.title,
            'due_time': r.due_time.strftime('%I:%M %p'),
            'call_on_due': r.call_on_due,
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
    """Get status or configure the Google Gemini API key."""
    from .services import update_gemini_api_key, is_valid_api_key
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    masked_key = f"{api_key[:6]}...{api_key[-4:]}" if len(api_key) > 12 else ("Configured" if is_valid_api_key(api_key) else "Not Configured")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_key = (data.get("api_key") or "").strip()
            if not new_key:
                return JsonResponse({"success": False, "error": "API key cannot be empty."}, status=400)
            ok, msg = update_gemini_api_key(new_key)
            return JsonResponse({
                "success": ok,
                "message": msg,
                "is_valid": is_valid_api_key(new_key),
                "masked_key": f"{new_key[:6]}...{new_key[-4:]}" if len(new_key) > 12 else "Saved",
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({
        "success": True,
        "is_configured": is_valid_api_key(api_key),
        "masked_key": masked_key,
        "model": getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash'),
    })
