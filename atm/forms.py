from django import forms
from .models import User


class LogInForm(forms.Form):
    card = forms.CharField(max_length=16)
    pin = forms.CharField(max_length=4)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'last_name', 'first_name', 'phone_number'
        ]
