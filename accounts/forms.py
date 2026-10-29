from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserPreference


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False, label='First Name')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        if commit:
            user.save()
        return user


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['response_style', 'voice_preference', 'voice_rate', 'voice_pitch',
                  'tts_enabled', 'history_enabled', 'notifications_enabled', 'timezone']
        widgets = {
            'voice_rate': forms.NumberInput(attrs={'step': '0.1', 'min': '0.5', 'max': '2.0'}),
            'voice_pitch': forms.NumberInput(attrs={'step': '0.1', 'min': '0.5', 'max': '2.0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault('class', 'form-select')
            else:
                field.widget.attrs.setdefault('class', 'form-control')
