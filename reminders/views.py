from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reminder


@login_required
def reminders_list_view(request):
    return redirect('home')


@login_required
def reminder_create_view(request):
    return redirect('home')


@login_required
def reminder_edit_view(request, reminder_id):
    return redirect('home')


@login_required
def reminder_complete_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.status = 'completed'
    reminder.save()
    messages.success(request, f'"{reminder.title}" marked as completed.')
    return redirect('home')


@login_required
def reminder_delete_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Reminder deleted.')
    return redirect('home')
