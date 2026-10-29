from django.contrib import admin
from .models import UserPreference

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'response_style', 'voice_preference', 'tts_enabled', 'history_enabled']
    list_filter = ['response_style', 'tts_enabled', 'history_enabled']
