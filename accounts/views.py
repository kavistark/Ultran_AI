from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register_view(request):
    return redirect('home')


def login_view(request):
    return redirect('home')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def preferences_view(request):
    return redirect('home')


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
    return redirect('home')
