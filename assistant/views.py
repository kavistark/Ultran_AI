from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone as django_timezone
from .models import Conversation, Message, ActionLog
from .services import chat_with_gemini
from accounts.models import UserPreference
from reminders.models import Reminder
import json


def home_view(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import login
    if not request.user.is_authenticated:
        kavi = User.objects.filter(username='kavi').first()
        if not kavi:
            kavi = User.objects.create_user('kavi', 'kavi@ai-ultran.local', 'kavi123', first_name='Kavi')
        login(request, kavi)

    user = request.user
    pref, _ = UserPreference.objects.get_or_create(user=user)
    upcoming_reminders = Reminder.objects.filter(user=user, status='pending').order_by('due_time')[:10]
    conversations = Conversation.objects.filter(user=user)[:10]
    documents = getattr(user, 'documents', None)
    doc_list = documents.all()[:10] if documents else []

    context = {
        'pref': pref,
        'upcoming_reminders': upcoming_reminders,
        'conversations': conversations,
        'documents': doc_list,
    }
    return render(request, 'voice_wave.html', context)


@login_required
def dashboard_view(request):
    pref, _ = UserPreference.objects.get_or_create(user=request.user)
    conversations = Conversation.objects.filter(user=request.user)[:5]
    upcoming_reminders = Reminder.objects.filter(
        user=request.user,
        status='pending',
    ).order_by('due_time')[:5]
    recent_actions = ActionLog.objects.filter(user=request.user)[:5]

    context = {
        'conversations': conversations,
        'upcoming_reminders': upcoming_reminders,
        'recent_actions': recent_actions,
        'pref': pref,
    }
    return render(request, 'dashboard.html', context)


@login_required
def assistant_view(request, conversation_id=None):
    pref, _ = UserPreference.objects.get_or_create(user=request.user)
    conversation = None

    if conversation_id:
        conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        msg_list = list(conversation.messages.values('role', 'content', 'timestamp', 'is_voice'))
    else:
        msg_list = []

    all_conversations = Conversation.objects.filter(user=request.user)[:20]

    context = {
        'conversation': conversation,
        'messages': msg_list,
        'all_conversations': all_conversations,
        'pref': pref,
    }
    return render(request, 'assistant.html', context)


@login_required
def history_view(request):
    conversations = Conversation.objects.filter(user=request.user)
    return render(request, 'history.html', {'conversations': conversations})


@login_required
def delete_conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted.')
    return redirect('history')


@login_required
def new_conversation_view(request):
    conv = Conversation.objects.create(user=request.user, title='New Conversation')
    return redirect('assistant_conversation', conversation_id=conv.id)


def voice_wave_view(request):
    from django.contrib.auth.models import User
    from django.contrib.auth import login
    if not request.user.is_authenticated:
        kavi = User.objects.filter(username='kavi').first()
        if not kavi:
            kavi = User.objects.create_user('kavi', 'kavi@ai-ultran.local', 'kavi123', first_name='Kavi')
        login(request, kavi)

    pref, _ = UserPreference.objects.get_or_create(user=request.user)
    upcoming_reminders = Reminder.objects.filter(user=request.user, status='pending').order_by('due_time')[:5]
    recent_conversations = Conversation.objects.filter(user=request.user)[:5]
    context = {
        'pref': pref,
        'upcoming_reminders': upcoming_reminders,
        'recent_conversations': recent_conversations,
    }
    return render(request, 'voice_wave.html', context)
