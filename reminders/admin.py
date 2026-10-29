from django.contrib import admin
from .models import Reminder

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'due_time', 'priority', 'status']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'user__username']
