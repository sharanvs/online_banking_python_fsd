from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Account
from finance_tools import calculate_emi

class BankingCoreTests(TestCase):
    def setUp(self):
        self.username = "tester"
        self.password = "strongpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.account = Account.objects.create(user=self.user, balance=Decimal("1000.00"))

    def test_login_and_dashboard(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        resp = self.client.get(reverse("dashboard"))
        self.assertEqual(resp.status_code, 200)

    def test_deposit(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post(reverse("deposit"), {"amount": "250.00"}, follow=True)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1250.00"))

    def test_withdraw_insufficient(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.post(reverse("withdraw"), {"amount": "2000.00"})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1000.00"))
        self.assertContains(resp, "Insufficient balance")

    def test_emi_function(self):
        emi = calculate_emi(100000, 10, 12)
        self.assertIsInstance(emi, float)
