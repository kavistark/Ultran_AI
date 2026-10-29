from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.reminders_api, name='reminders_api'),
    path('<int:reminder_id>/', api_views.reminder_detail_api, name='reminder_detail_api'),
]
