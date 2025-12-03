from decimal import Decimal
from joblib import load
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import (
    RegisterForm, DepositForm, WithdrawForm, SIPForm, FDForm, RDForm, RetirementForm,
    HomeLoanEligibilityForm, CreditCardForm, TaxableIncomeForm, BudgetForm, NetWorthForm
)
from .models import Account
from finance_tools import (
    calculate_emi, calculate_sip, calculate_fd, calculate_rd, estimate_retirement_corpus,
    estimate_home_loan_eligibility, calculate_credit_card_balance, calculate_taxable_income,
    plan_budget, calculate_net_worth
)

def index(request):
    return render(request, "bank_app/index.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            Account.objects.create(user=user)
            user = authenticate(username=user.username, password=password)
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "bank_app/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "bank_app/login.html", {"form": form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("index")

@login_required
def dashboard(request):
    account, _ = Account.objects.get_or_create(user=request.user)
    transactions = account.transactions.all()[:10]
    return render(request, "bank_app/dashboard.html", {"account": account, "transactions": transactions})

@login_required
def deposit(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = Decimal(form.cleaned_data["amount"])
            account.deposit(amount)
            return redirect("dashboard")
    else:
        form = DepositForm()
    return render(request, "bank_app/deposit.html", {"form": form, "account": account})

@login_required
def withdraw(request):
    account = get_object_or_404(Account, user=request.user)
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            amount = Decimal(form.cleaned_data["amount"])
            try:
                account.withdraw(amount)
                return redirect("dashboard")
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = WithdrawForm()
    return render(request, "bank_app/withdraw.html", {"form": form, "account": account})

# Tools views
@login_required
def tools_menu(request):
    return render(request, "bank_app/tools_menu.html")

@login_required
def emi_tool(request):
    result = None
    errors = None
    if request.method == "GET":
        p = request.GET.get("principal")
        r = request.GET.get("rate")
        n = request.GET.get("months")
        if p and r and n:
            try:
                result = calculate_emi(float(p), float(r), int(n))
            except Exception as exc:
                errors = str(exc)
    return render(request, "bank_app/emi_tool.html", {"result": result, "errors": errors})

@login_required
def sip_tool(request):
    result = None
    form = SIPForm(request.GET or None)
    if form.is_valid():
        result = calculate_sip(form.cleaned_data["monthly_investment"],
                               form.cleaned_data["annual_rate_percent"],
                               form.cleaned_data["years"])
    return render(request, "bank_app/sip_tool.html", {"form": form, "result": result})

@login_required
def fd_tool(request):
    result = None
    form = FDForm(request.GET or None)
    if form.is_valid():
        result = calculate_fd(form.cleaned_data["principal"],
                              form.cleaned_data["annual_rate_percent"],
                              form.cleaned_data["years"],
                              form.cleaned_data["compounding_per_year"])
    return render(request, "bank_app/fd_tool.html", {"form": form, "result": result})

@login_required
def rd_tool(request):
    result = None
    form = RDForm(request.GET or None)
    if form.is_valid():
        result = calculate_rd(form.cleaned_data["monthly_deposit"],
                              form.cleaned_data["annual_rate_percent"],
                              form.cleaned_data["years"])
    return render(request, "bank_app/rd_tool.html", {"form": form, "result": result})

@login_required
def retirement_tool(request):
    result = None
    form = RetirementForm(request.GET or None)
    if form.is_valid():
        result = estimate_retirement_corpus(form.cleaned_data["current_savings"],
                                            form.cleaned_data["monthly_addition"],
                                            form.cleaned_data["annual_return_percent"],
                                            form.cleaned_data["years"])
    return render(request, "bank_app/retirement_tool.html", {"form": form, "result": result})

@login_required
def loan_eligibility_tool(request):
    result = None
    form = HomeLoanEligibilityForm(request.GET or None)
    if form.is_valid():
        result = estimate_home_loan_eligibility(form.cleaned_data["monthly_income"],
                                               form.cleaned_data["monthly_expenses"],
                                               form.cleaned_data["annual_rate_percent"],
                                               form.cleaned_data["max_tenure_years"],
                                               form.cleaned_data["permissible_emi_fraction"])
    return render(request, "bank_app/loan_eligibility_tool.html", {"form": form, "result": result})

@login_required
def credit_card_tool(request):
    result = None
    form = CreditCardForm(request.GET or None)
    if form.is_valid():
        result = calculate_credit_card_balance(form.cleaned_data["initial_balance"],
                                               form.cleaned_data["annual_rate_percent"],
                                               form.cleaned_data["min_payment_percent"],
                                               form.cleaned_data["months"])
    return render(request, "bank_app/credit_card_tool.html", {"form": form, "result": result})

@login_required
def taxable_income_tool(request):
    result = None
    form = TaxableIncomeForm(request.GET or None)
    if form.is_valid():
        result = calculate_taxable_income(form.cleaned_data["gross_income"],
                                          form.cleaned_data["standard_deduction"],
                                          form.cleaned_data["other_deductions"],
                                          form.cleaned_data.get("deduction_cap"))
    return render(request, "bank_app/taxable_income_tool.html", {"form": form, "result": result})

@login_required
def budget_tool(request):
    result = None
    form = BudgetForm(request.GET or None)
    if form.is_valid():
        result = plan_budget(form.cleaned_data["monthly_income"], form.cleaned_data["monthly_expenses"])
    return render(request, "bank_app/budget_tool.html", {"form": form, "result": result})

@login_required
def net_worth_tool(request):
    result = None
    form = NetWorthForm(request.GET or None)
    if form.is_valid():
        assets = [float(x.strip()) for x in form.cleaned_data["assets"].split(",") if x.strip()]
        liabilities = [float(x.strip()) for x in form.cleaned_data["liabilities"].split(",") if x.strip()]
        result = calculate_net_worth(assets, liabilities)
    return render(request, "bank_app/net_worth_tool.html", {"form": form, "result": result})
model = load("ml/loan_amount_model.joblib")

@login_required
def loan_estimator(request):
    predicted_amount = None

    if request.method == "POST":
        age = int(request.POST.get("age", 0))
        income = float(request.POST.get("monthly_income", 0))
        score = int(request.POST.get("credit_score", 0))
        tenure = int(request.POST.get("loan_tenure", 0))
        existing = float(request.POST.get("existing_loan", 0))
        deps = int(request.POST.get("dependents", 0))

        # Build DataFrame with the exact feature names expected by the model
        features_df = pd.DataFrame(
            [[age, income, score, tenure, existing, deps]],
            columns=[
                "Age",
                "Monthly_Income",
                "Credit_Score",
                "Loan_Tenure_Years",
                "Existing_Loan_Amount",
                "Num_of_Dependents",
            ],
        )

        try:
            predicted_amount = int(model.predict(features_df)[0])
        except Exception:
            predicted_amount = None

    return render(request, "bank_app/loan_estimator.html", {
        "predicted_amount": predicted_amount
    })

