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
        'user': user,
        'pref': pref,
        'upcoming_reminders': upcoming_reminders,
        'conversations': conversations,
        'documents': doc_list,
    }
    return render(request, 'voice_wave.html', context)


@login_required
def dashboard_view(request):
    return home_view(request)


@login_required
def assistant_view(request, conversation_id=None):
    if conversation_id:
        get_object_or_404(Conversation, id=conversation_id, user=request.user)
    return home_view(request)


@login_required
def history_view(request):
    return redirect('home')


@login_required
def delete_conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    if request.method == 'POST':
        conversation.delete()
        messages.success(request, 'Conversation deleted.')
    return redirect('home')


@login_required
def new_conversation_view(request):
    return redirect('home')


def voice_wave_view(request):
    return home_view(request)
