from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat_api, name='chat_api'),
    path('conversations/', api_views.conversations_api, name='conversations_api'),
    path('conversations/<int:conversation_id>/messages/', api_views.messages_api, name='messages_api'),
    path('history/delete-all/', api_views.delete_all_history_api, name='delete_all_history'),
    path('reminders/due/', api_views.due_reminders_api, name='due_reminders_api'),
    path('contacts/', api_views.contacts_api, name='contacts_api'),
    path('tts/', api_views.tts_api, name='tts_api'),
    path('stt/', api_views.stt_api, name='stt_api'),
    path('config/gemini-key/', api_views.configure_gemini_key_api, name='configure_gemini_key_api'),
]
