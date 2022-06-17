from django.urls import path
from . import views

app_name = 'atm'
urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', views.user_registration, name='registration'),
    path('login/', views.user_login, name='login'),
    path('register/created/', views.created, name='created'),
    path('logout/', views.user_logout, name='logout'),
    path('balance/', views.balance, name='balance'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('send-money/', views.send_money, name='send_money'),
    path('new-card/', views.new_card, name='new_card'),
    path('change-pin/', views.change_pin, name='change_pin'),
]
