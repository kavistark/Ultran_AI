from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from assistant.models import ActionLog


@login_required
def integrations_view(request):
    action_logs = ActionLog.objects.filter(user=request.user)[:20]
    return render(request, 'integrations/list.html', {'action_logs': action_logs})
