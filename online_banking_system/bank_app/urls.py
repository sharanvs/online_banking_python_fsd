from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("tools/", views.tools_menu, name="tools_menu"),
    path("tools/emi/", views.emi_tool, name="emi_tool"),
    path("tools/sip/", views.sip_tool, name="sip_tool"),
    path("tools/fd/", views.fd_tool, name="fd_tool"),
    path("tools/rd/", views.rd_tool, name="rd_tool"),
    path("tools/retirement/", views.retirement_tool, name="retirement_tool"),
    path("tools/loan-eligibility/", views.loan_eligibility_tool, name="loan_eligibility_tool"),
    path("tools/credit-card/", views.credit_card_tool, name="credit_card_tool"),
    path("tools/taxable-income/", views.taxable_income_tool, name="taxable_income_tool"),
    path("tools/budget/", views.budget_tool, name="budget_tool"),
    path("tools/net-worth/", views.net_worth_tool, name="net_worth_tool"),
    path("tools/loan-prediction/", views.loan_estimator, name="loan_estimator"),
]
