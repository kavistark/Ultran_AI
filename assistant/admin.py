from django.contrib import admin
from .models import Conversation, Message, ActionLog


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['timestamp']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'updated_at']
    list_filter = ['user']
    inlines = [MessageInline]


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action_type', 'status', 'timestamp']
    list_filter = ['status', 'action_type']
    readonly_fields = ['timestamp']
