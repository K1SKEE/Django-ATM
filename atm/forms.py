from django import forms
from .models import User, Wallet, Card


class LogInForm(forms.Form):
    card = forms.CharField(max_length=16)
    pin = forms.CharField(max_length=4)


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'last_name', 'first_name', 'phone_number'
        ]


class ChangePinForm(forms.Form):
    pin1 = forms.CharField(max_length=4)
    pin2 = forms.CharField(max_length=4)


class DepositForm(forms.Form):
    value = forms.IntegerField()

    class Meta:
        model = User
        fields = ['wallet']


class WithdrawForm(forms.Form):
    value = forms.IntegerField()


class SelectCardForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ['card']


class OpenNewCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['currency']
