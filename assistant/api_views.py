import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone as django_timezone
from .models import Conversation, Message, ActionLog
from .services import chat_with_gemini
from accounts.models import UserPreference
from reminders.models import Reminder
from integrations.permissions import is_action_allowed


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    try:
        if not request.user.is_authenticated:
            from django.contrib.auth.models import User
            from django.contrib.auth import login
            kavi = User.objects.filter(username='kavi').first()
            if not kavi:
                kavi = User.objects.create_user('kavi', 'kavi@ai-ultran.local', 'kavi123', first_name='Kavi')
            login(request, kavi)

        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        is_voice = data.get('is_voice', False)

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
            # Append action confirmation to response
            if action_result.get('message'):
                response_text = (response_text + '\n\n' + action_result['message']).strip()

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
            'message': f"⚠️ Security Notice: Action '{intent}' is not permitted by AI ULTRAN's action controller allowlist.",
        }

    ActionLog.objects.create(
        user=user,
        action_type=intent,
        status='approved',
        details=action,
    )

    if intent == 'create_reminder':
        try:
            from reminders.models import Reminder
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
                    'message': f'✅ Reminder created: "{title}" for {due_time.strftime("%B %d, %Y at %I:%M %p")}',
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

    return {'success': True, 'message': ''}


@login_required
@require_http_methods(["GET"])
def conversations_api(request):
    conversations = Conversation.objects.filter(user=request.user).values(
        'id', 'title', 'created_at', 'updated_at'
    )
    return JsonResponse({'conversations': list(conversations)})


@login_required
@require_http_methods(["GET"])
def messages_api(request, conversation_id):
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        msgs = conversation.messages.values('id', 'role', 'content', 'timestamp', 'is_voice')
        return JsonResponse({'messages': list(msgs)})
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found.'}, status=404)


@login_required
@require_http_methods(["DELETE"])
def delete_all_history_api(request):
    Conversation.objects.filter(user=request.user).delete()
    return JsonResponse({'success': True, 'message': 'All conversation history deleted.'})
