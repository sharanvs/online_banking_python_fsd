from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("account", "tx_type", "amount", "timestamp")
