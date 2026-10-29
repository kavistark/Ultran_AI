from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from assistant.models import ActionLog


@login_required
def integrations_view(request):
    return redirect('home')
