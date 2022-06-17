from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LogInForm, RegisterForm, ChangePinForm, DepositForm, \
    WithdrawForm, OpenNewCardForm, SelectCardForm
from .models import User, Card
import requests


# Create your views here.
def index(request, context=None):
    return render(request, 'ATM/index.html', concatenated_context(context))


def user_registration(request):
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            context['user'] = user
            return render(request, 'ATM/created.html',
                          concatenated_context(context))
    else:
        form = RegisterForm()
    context['form'] = form
    return render(request, 'ATM/registration.html',
                  concatenated_context(context))


def user_login(request):
    access = False
    context = {}
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['card']
            password = form.cleaned_data['pin']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                access = True
                success_text = "Ви успішно увійшли в систему."
                context['success_text'] = success_text
                context['user'] = user
            else:
                form = LogInForm()
                err_message = 'Неправильная пара логин/пароль'
                context['err_message'] = err_message
    else:
        form = LogInForm()
    context['form'] = form
    return redirect('atm:index') \
        if access else render(request, 'ATM/login.html',
                              concatenated_context(context))


def user_logout(request):
    logout(request)
    return redirect('atm:index')


def created(request):
    return render(request, 'ATM/created.html')


def balance(request):
    context = {
        'balance': request.user.wallet.card.balance,
        'card': request.user.wallet.card.card_number,
        'currency': request.user.wallet.card.currency,
    }
    if request.method == 'POST':
        form = SelectCardForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data['card']
    else:
        form = SelectCardForm()
    context['form'] = form
    return render(request, 'ATM/balance.html', concatenated_context(context))


def deposit(request):
    context = {}
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            request.user.wallet.card.deposit(value)
            context['message'] = f'Баланс поповнено на {value} \
                                    {request.user.wallet.card.get_currency()}'
    else:
        form = DepositForm()
    context['form'] = form
    return render(request, 'ATM/deposit.html', concatenated_context(context))


def withdraw(request):
    context = {}
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['value']
            message = request.user.wallet.card.withdraw(value)
            context['message'] = message
    else:
        form = WithdrawForm()
    context['form'] = form
    return render(request, 'ATM/withdraw.html', concatenated_context(context))


def send_money(request):
    context = {}
    return render(request, '', concatenated_context(context))


def new_card(request):
    context = {}
    if request.method == 'POST':
        form = OpenNewCardForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            card = Card()
            card.create_card()
            card.currency = currency
            card.save()
            request.user.wallet.card = card
    else:
        form = OpenNewCardForm()
    context['form'] = form
    return render(request, 'ATM/new_card.html', concatenated_context(context))


def change_pin(request):
    context = {}
    if request.method == 'POST':
        form = ChangePinForm(request.POST)
        if form.is_valid():
            pin1, pin2 = form.cleaned_data['pin1'], form.cleaned_data['pin2']
            if pin1 == pin2:
                context['message'] = 'PIN-код успішно змінений'
                request.user.set_password(pin2)
                request.user.save()
            else:
                context['message'] = 'pin 1 != pin 2'
    else:
        form = ChangePinForm()
    context['form'] = form
    return render(request, 'ATM/change_pin.html', concatenated_context(context))


def get_currency_rate():
    exchange_rate_json = requests.get(
        'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    ).json()
    usd_buy = exchange_rate_json[0]['buy']
    usd_sale = exchange_rate_json[0]['sale']
    eur_buy = exchange_rate_json[1]['buy']
    eur_sale = exchange_rate_json[1]['sale']
    context = {
        'usd': [usd_buy, usd_sale],
        'eur': [eur_buy, eur_sale],
    }
    return context


def concatenated_context(context):
    if context:
        return get_currency_rate() | context
    return get_currency_rate()
