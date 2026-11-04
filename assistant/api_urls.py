from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat_api, name='chat_api'),
    path('conversations/', api_views.conversations_api, name='conversations_api'),
    path('conversations/<int:conversation_id>/messages/', api_views.messages_api, name='messages_api'),
    path('history/delete-all/', api_views.delete_all_history_api, name='delete_all_history'),
    path('reminders/due/', api_views.due_reminders_api, name='due_reminders_api'),
    path('reminders/test-call/', api_views.test_call_api, name='test_call_api'),
    path('config/phone-number/', api_views.configure_phone_api, name='configure_phone_api'),
    path('contacts/', api_views.contacts_api, name='contacts_api'),
    path('tts/', api_views.tts_api, name='tts_api'),
    path('stt/', api_views.stt_api, name='stt_api'),
    path('config/gemini-key/', api_views.configure_gemini_key_api, name='configure_gemini_key_api'),
    path('device/status/', api_views.device_status_api, name='device_status_api'),
    path('device/action/', api_views.device_action_api, name='device_action_api'),
    path('device/screen/inspect/', api_views.inspect_screen_api, name='inspect_screen_api'),
]
