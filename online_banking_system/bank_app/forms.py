from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password_confirm")
        if pw and pw2 and pw != pw2:
            self.add_error("password_confirm", "Passwords do not match.")
        return cleaned

class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2, min_value=0.01)

# Tool forms:
class SIPForm(forms.Form):
    monthly_investment = forms.FloatField(min_value=0)
    annual_rate_percent = forms.FloatField(min_value=0)
    years = forms.FloatField(min_value=0)

class FDForm(forms.Form):
    principal = forms.FloatField(min_value=0)
    annual_rate_percent = forms.FloatField(min_value=0)
    years = forms.FloatField(min_value=0)
    compounding_per_year = forms.IntegerField(min_value=1, initial=1)

class RDForm(forms.Form):
    monthly_deposit = forms.FloatField(min_value=0)
    annual_rate_percent = forms.FloatField(min_value=0)
    years = forms.FloatField(min_value=0)

class RetirementForm(forms.Form):
    current_savings = forms.FloatField(min_value=0)
    monthly_addition = forms.FloatField(min_value=0)
    annual_return_percent = forms.FloatField(min_value=0)
    years = forms.FloatField(min_value=0)

class HomeLoanEligibilityForm(forms.Form):
    monthly_income = forms.FloatField(min_value=0)
    monthly_expenses = forms.FloatField(min_value=0)
    annual_rate_percent = forms.FloatField(min_value=0)
    max_tenure_years = forms.IntegerField(min_value=1)
    permissible_emi_fraction = forms.FloatField(min_value=0, max_value=1, initial=0.5)

class CreditCardForm(forms.Form):
    initial_balance = forms.FloatField(min_value=0)
    annual_rate_percent = forms.FloatField(min_value=0)
    min_payment_percent = forms.FloatField(min_value=0, max_value=100)
    months = forms.IntegerField(min_value=0)

class TaxableIncomeForm(forms.Form):
    gross_income = forms.FloatField(min_value=0)
    standard_deduction = forms.FloatField(min_value=0, initial=12500)
    other_deductions = forms.FloatField(min_value=0, initial=0)
    deduction_cap = forms.FloatField(required=False, min_value=0)

class BudgetForm(forms.Form):
    monthly_income = forms.FloatField(min_value=0)
    monthly_expenses = forms.FloatField(min_value=0)

class NetWorthForm(forms.Form):
    assets = forms.CharField(help_text="Comma-separated asset values (e.g., 50000, 20000)")
    liabilities = forms.CharField(help_text="Comma-separated liability values (e.g., 10000, 5000)")
