from random import randint

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        """
        Создает и сохраняет пользователя с автоматически сгенерированным
        номером карты и используемым в качестве логина.
        """
        user = self.model(password=password, **extra_fields)
        username = self._create_card()
        user.create_iban()
        user.username = username
        user.card_id = username
        user.atm = ATM.objects.get(pk=1)
        # user.add_card(username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, password='0000', **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(password, **extra_fields)

    @staticmethod
    def _create_card():
        card = Card()
        card.create_card()
        card.save()
        return card.card_number


class ATM(models.Model):
    objects = models.Manager()
    balance = models.PositiveIntegerField(
        default=0,
        verbose_name='Баланс доступної готівки в банкоматі'
    )

    def __str__(self):
        return str(self.balance)


class Card(models.Model):
    TYPES_CURRENCY = [
        ('UAH', 'Гривня'),
        ('USD', 'Долар США'),
        ('EUR', 'Євро'),
    ]
    objects = models.Manager()
    card_number = models.CharField(
        max_length=16,
        unique=True, primary_key=True,
        verbose_name='Номер карти'
    )
    currency = models.CharField(
        max_length=3,
        choices=TYPES_CURRENCY,
        default='UAH',
        verbose_name='Валюта карти'
    )
    balance = models.PositiveIntegerField(
        default=0,
        verbose_name='Баланс карти'
    )

    def __str__(self):
        return self.card_number

    def create_card(self):
        random_card = [str(randint(0, 9)) for _ in range(12)]
        new_card = '4149' + ''.join(random_card)
        self.card_number = new_card
        return self.card_number

    def get_balance(self):
        return str(self.balance)

    def get_card_number(self):
        return self.card_number

    def get_currency(self):
        return self.currency

    def _deposit(self, value):
        pass

    def _withdraw(self, value):
        pass


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    objects = UserManager()
    username = models.CharField(
        _("Номер карти"),
        max_length=16,
        unique=True,
        validators=[username_validator]
    )
    iban = models.CharField(
        max_length=30, unique=True,
        verbose_name='Номер рахунку IBAN',
        primary_key=True
    )
    password = models.CharField(
        _("PIN-код"),
        max_length=4, default='0000'
    )
    card = models.OneToOneField(
        Card,
        on_delete=models.PROTECT,
        null=True
    )
    last_name = models.CharField(
        max_length=30,
        verbose_name='Прізвище'
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Ім\'я'
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Фінансовий номер телефону'
    )
    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата відкриття рахунку'
    )
    time_update = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата оновлення даних'
    )
    is_active = models.BooleanField(
        _('is_active'),
        default=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    atm = models.ForeignKey(
        ATM,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def create_iban(self):
        country = 'UA'
        code = '0000'
        random_iban = [str(randint(0, 9)) for _ in range(12)]
        new_iban = country + code + ''.join(random_iban)
        self.iban = new_iban
        return self.iban

    # def add_card(self, card_id):
    #     card = Card.objects.get(card_number=card_id)
    #     return self.wallet.__setattr__(card.currency, card.card_number)
