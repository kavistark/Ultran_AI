from django.db import models
from django.contrib.auth.models import User


class UserPreference(models.Model):
    RESPONSE_STYLE_CHOICES = [
        ('concise', 'Concise'),
        ('detailed', 'Detailed'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
    ]
    VOICE_CHOICES = [
        ('default', 'Default'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    response_style = models.CharField(max_length=20, choices=RESPONSE_STYLE_CHOICES, default='concise')
    voice_preference = models.CharField(max_length=20, choices=VOICE_CHOICES, default='male')
    voice_rate = models.FloatField(default=1.0)
    voice_pitch = models.FloatField(default=1.0)
    tts_enabled = models.BooleanField(default=True)
    history_enabled = models.BooleanField(default=True)
    notifications_enabled = models.BooleanField(default=True)
    timezone = models.CharField(max_length=50, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
