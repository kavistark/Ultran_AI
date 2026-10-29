from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reminder
from .forms import ReminderForm


@login_required
def reminders_list_view(request):
    pending = Reminder.objects.filter(user=request.user, status='pending').order_by('due_time')
    completed = Reminder.objects.filter(user=request.user, status='completed').order_by('-updated_at')[:10]
    return render(request, 'reminders/list.html', {
        'pending': pending,
        'completed': completed,
    })


@login_required
def reminder_create_view(request):
    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.user = request.user
            reminder.save()
            messages.success(request, f'Reminder "{reminder.title}" created.')
            return redirect('reminders_list')
    else:
        form = ReminderForm()
    return render(request, 'reminders/form.html', {'form': form, 'action': 'Create'})


@login_required
def reminder_edit_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reminder updated.')
            return redirect('reminders_list')
    else:
        form = ReminderForm(instance=reminder)
    return render(request, 'reminders/form.html', {'form': form, 'action': 'Edit', 'reminder': reminder})


@login_required
def reminder_complete_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.status = 'completed'
    reminder.save()
    messages.success(request, f'"{reminder.title}" marked as completed.')
    return redirect('reminders_list')


@login_required
def reminder_delete_view(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    if request.method == 'POST':
        reminder.delete()
        messages.success(request, 'Reminder deleted.')
    return redirect('reminders_list')
