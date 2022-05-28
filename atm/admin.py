from django.contrib import admin
from .models import Card, User, ATM

# Register your models here.
admin.site.register(Card)
admin.site.register(User)
admin.site.register(ATM)
