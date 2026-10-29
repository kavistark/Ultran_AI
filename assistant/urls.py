from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('voice/', views.voice_wave_view, name='voice_wave'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('assistant/', views.assistant_view, name='assistant'),
    path('assistant/<int:conversation_id>/', views.assistant_view, name='assistant_conversation'),
    path('assistant/new/', views.new_conversation_view, name='new_conversation'),
    path('history/', views.history_view, name='history'),
    path('history/<int:conversation_id>/delete/', views.delete_conversation_view, name='delete_conversation'),
]
