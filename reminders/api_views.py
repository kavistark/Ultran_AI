import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Reminder


@login_required
@require_http_methods(["GET", "POST"])
def reminders_api(request):
    if request.method == 'GET':
        reminders = Reminder.objects.filter(user=request.user, status='pending').values(
            'id', 'title', 'description', 'due_time', 'priority', 'status'
        )
        return JsonResponse({'reminders': list(reminders)})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reminder = Reminder.objects.create(
                user=request.user,
                title=data['title'],
                description=data.get('description', ''),
                due_time=data['due_time'],
                priority=data.get('priority', 'medium'),
            )
            return JsonResponse({'id': reminder.id, 'title': reminder.title}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_http_methods(["PATCH", "DELETE"])
def reminder_detail_api(request, reminder_id):
    try:
        reminder = Reminder.objects.get(id=reminder_id, user=request.user)
    except Reminder.DoesNotExist:
        return JsonResponse({'error': 'Not found.'}, status=404)

    if request.method == 'DELETE':
        reminder.delete()
        return JsonResponse({'success': True})

    if request.method == 'PATCH':
        data = json.loads(request.body)
        for field in ['title', 'description', 'priority', 'status']:
            if field in data:
                setattr(reminder, field, data[field])
        reminder.save()
        return JsonResponse({'success': True})
