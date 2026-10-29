from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminders_list_view, name='reminders_list'),
    path('create/', views.reminder_create_view, name='reminder_create'),
    path('<int:reminder_id>/edit/', views.reminder_edit_view, name='reminder_edit'),
    path('<int:reminder_id>/complete/', views.reminder_complete_view, name='reminder_complete'),
    path('<int:reminder_id>/delete/', views.reminder_delete_view, name='reminder_delete'),
]
