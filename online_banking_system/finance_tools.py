from typing import List
from math import pow


def _positive_number(name: str, value):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number (int or float).")
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def calculate_emi(principal: float, annual_rate_percent: float, tenure_months: int) -> float:
    """Monthly EMI for a loan."""
    _positive_number("principal", principal)
    _positive_number("annual_rate_percent", annual_rate_percent)
    if not isinstance(tenure_months, int) or tenure_months <= 0:
        raise ValueError("tenure_months must be a positive integer.")
    if annual_rate_percent == 0:
        return float(principal) / tenure_months
    monthly_rate = annual_rate_percent / 100.0 / 12.0
    r = monthly_rate
    n = tenure_months
    emi = principal * r * pow(1 + r, n) / (pow(1 + r, n) - 1)
    return float(emi)


def calculate_sip(monthly_investment: float, annual_rate_percent: float, years: float) -> float:
    """SIP maturity amount (end-of-period contributions)."""
    _positive_number("monthly_investment", monthly_investment)
    _positive_number("annual_rate_percent", annual_rate_percent)
    _positive_number("years", years)
    months = int(round(years * 12))
    if months == 0:
        return 0.0
    r = annual_rate_percent / 100.0 / 12.0
    if r == 0:
        return monthly_investment * months
    fv_factor = (pow(1 + r, months) - 1) / r
    maturity = monthly_investment * fv_factor
    return float(maturity)


def calculate_fd(principal: float, annual_rate_percent: float, years: float, compounding_per_year: int = 1) -> float:
    """Fixed deposit maturity with compounding."""
    _positive_number("principal", principal)
    _positive_number("annual_rate_percent", annual_rate_percent)
    _positive_number("years", years)
    if not isinstance(compounding_per_year, int) or compounding_per_year < 1:
        raise ValueError("compounding_per_year must be integer >= 1.")
    r = annual_rate_percent / 100.0
    n = compounding_per_year
    t = years
    maturity = principal * pow(1 + r / n, n * t)
    return float(maturity)


def calculate_rd(monthly_deposit: float, annual_rate_percent: float, years: float) -> float:
    """Recurring deposit maturity by monthly simulation."""
    _positive_number("monthly_deposit", monthly_deposit)
    _positive_number("annual_rate_percent", annual_rate_percent)
    _positive_number("years", years)
    months = int(round(years * 12))
    if months == 0:
        return 0.0
    monthly_rate = annual_rate_percent / 100.0 / 12.0
    amount = 0.0
    for _ in range(months):
        amount = (amount + monthly_deposit) * (1 + monthly_rate)
    return float(amount)


def estimate_retirement_corpus(current_savings: float,
                               monthly_addition: float,
                               annual_return_percent: float,
                               years: float) -> float:
    """Project retirement corpus with monthly additions."""
    _positive_number("current_savings", current_savings)
    _positive_number("monthly_addition", monthly_addition)
    _positive_number("annual_return_percent", annual_return_percent)
    _positive_number("years", years)
    months = int(round(years * 12))
    if months == 0:
        return float(current_savings)
    monthly_rate = annual_return_percent / 100.0 / 12.0
    amount = float(current_savings)
    for _ in range(months):
        amount = amount * (1 + monthly_rate) + monthly_addition
    return float(amount)


def estimate_home_loan_eligibility(monthly_income: float,
                                   monthly_expenses: float,
                                   annual_rate_percent: float,
                                   max_tenure_years: int,
                                   permissible_emi_fraction: float = 0.5) -> float:
    """Estimate max home loan principal based on available EMI capacity."""
    _positive_number("monthly_income", monthly_income)
    _positive_number("monthly_expenses", monthly_expenses)
    _positive_number("annual_rate_percent", annual_rate_percent)
    if not isinstance(max_tenure_years, int) or max_tenure_years <= 0:
        raise ValueError("max_tenure_years must be positive integer.")
    if not (0 <= permissible_emi_fraction <= 1):
        raise ValueError("permissible_emi_fraction must be between 0 and 1.")
    net_available = monthly_income - monthly_expenses
    if net_available <= 0:
        return 0.0
    allowed_emi = net_available * permissible_emi_fraction
    n = max_tenure_years * 12
    if annual_rate_percent == 0:
        return allowed_emi * n
    r = annual_rate_percent / 100.0 / 12.0
    principal = allowed_emi * (1 - pow(1 + r, -n)) / r
    return float(principal)


def calculate_credit_card_balance(initial_balance: float,
                                  annual_rate_percent: float,
                                  min_payment_percent: float,
                                  months: int) -> float:
    """Simulate credit card outstanding after paying minimum each month."""
    _positive_number("initial_balance", initial_balance)
    _positive_number("annual_rate_percent", annual_rate_percent)
    _positive_number("min_payment_percent", min_payment_percent)
    if not isinstance(months, int) or months < 0:
        raise ValueError("months must be non-negative integer.")
    if not (0 <= min_payment_percent <= 100):
        raise ValueError("min_payment_percent must be between 0 and 100.")
    balance = float(initial_balance)
    monthly_rate = annual_rate_percent / 100.0 / 12.0
    for _ in range(months):
        balance = balance * (1 + monthly_rate)
        min_payment = balance * (min_payment_percent / 100.0)
        payment = min(min_payment, balance)
        balance = balance - payment
    return float(balance)


def calculate_taxable_income(gross_income: float,
                             standard_deduction: float = 12500.0,
                             other_deductions: float = 0.0,
                             deduction_cap: float = None) -> float:
    """Compute taxable income after deductions."""
    _positive_number("gross_income", gross_income)
    _positive_number("standard_deduction", standard_deduction)
    _positive_number("other_deductions", other_deductions)
    if deduction_cap is not None:
        _positive_number("deduction_cap", deduction_cap)
    total_deductions = standard_deduction + other_deductions
    if deduction_cap is not None:
        total_deductions = min(total_deductions, deduction_cap)
    taxable = gross_income - total_deductions
    return float(taxable if taxable > 0 else 0.0)


def plan_budget(monthly_income: float, monthly_expenses: float) -> dict:
    """Suggest savings/investment buckets based on income vs expenses."""
    _positive_number("monthly_income", monthly_income)
    _positive_number("monthly_expenses", monthly_expenses)
    if monthly_income == 0:
        return {
            "income": 0.0,
            "expenses": float(monthly_expenses),
            "suggested_savings": 0.0,
            "suggested_investment": 0.0,
            "advice": "No income — seek income sources or assistance."
        }
    available = monthly_income - monthly_expenses
    if available <= 0:
        advice = ("Expenses meet or exceed income. Reduce discretionary spending, consolidate debts, or increase income.")
        return {
            "income": float(monthly_income),
            "expenses": float(monthly_expenses),
            "suggested_savings": 0.0,
            "suggested_investment": 0.0,
            "advice": advice
        }
    emergency = available * 0.20
    long_term = available * 0.30
    flexible = available - emergency - long_term
    return {
        "income": float(monthly_income),
        "expenses": float(monthly_expenses),
        "suggested_savings": round(emergency + flexible, 2),
        "suggested_investment": round(long_term, 2),
        "advice": ("Allocate ~20% to emergency savings, ~30% to long-term investments, rest to flexible savings or debt repayment.")
    }


def calculate_net_worth(assets: List[float], liabilities: List[float]) -> float:
    """Net worth = sum(assets) - sum(liabilities)."""
    if not isinstance(assets, list) or not isinstance(liabilities, list):
        raise TypeError("assets and liabilities must be lists of numbers.")
    for i, a in enumerate(assets):
        _positive_number(f"assets[{i}]", a)
    for i, l in enumerate(liabilities):
        _positive_number(f"liabilities[{i}]", l)
    return float(sum(assets) - sum(liabilities))
