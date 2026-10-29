from django.urls import path
from . import api_views

urlpatterns = [
    path('chat/', api_views.chat_api, name='chat_api'),
    path('conversations/', api_views.conversations_api, name='conversations_api'),
    path('conversations/<int:conversation_id>/messages/', api_views.messages_api, name='messages_api'),
    path('history/delete-all/', api_views.delete_all_history_api, name='delete_all_history'),
]
