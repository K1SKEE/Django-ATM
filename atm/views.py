from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LogInForm, RegisterForm
from .models import User
import requests


# Create your views here.
def index(request, context=None):
    return render(request, 'ATM/index.html', concatenated_context(context))


def user_registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            context = {
                'user': user
            }
            return render(request, 'ATM/created.html',
                          concatenated_context(context))
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
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
                success_text = "Вы успешно вошли в систему."
                context['success_text'] = success_text
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
    pass


def deposit(request):
    pass


def withdraw(request):
    pass


def send_money(request):
    pass


def new_card(request):
    pass


def change_pin(request):
    pass


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
