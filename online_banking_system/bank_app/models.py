from django.conf import settings
from django.db import models
from decimal import Decimal

class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()
        Transaction.objects.create(account=self, amount=amount, tx_type=Transaction.DEPOSIT)

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(account=self, amount=amount, tx_type=Transaction.WITHDRAWAL)

    def __str__(self):
        return f"Account({self.user.username}): {self.balance}"


class Transaction(models.Model):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TX_CHOICES = [(DEPOSIT, "Deposit"), (WITHDRAWAL, "Withdrawal")]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tx_type = models.CharField(max_length=20, choices=TX_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.tx_type} {self.amount} on {self.timestamp}"
