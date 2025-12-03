import unittest
from finance_tools import (
    calculate_emi, calculate_sip, calculate_fd, calculate_rd,
    estimate_retirement_corpus, estimate_home_loan_eligibility,
    calculate_credit_card_balance, calculate_taxable_income,
    plan_budget, calculate_net_worth
)

class TestFinanceTools(unittest.TestCase):
    def test_emi_zero_interest(self):
        self.assertAlmostEqual(calculate_emi(120000, 0, 12), 10000.0)

    def test_emi_positive(self):
        emi = calculate_emi(100000, 10, 12)
        self.assertIsInstance(emi, float)
        self.assertGreater(emi, 0)

    def test_sip_zero_rate(self):
        self.assertEqual(calculate_sip(500, 0, 2), 500 * 24)

    def test_fd(self):
        self.assertAlmostEqual(calculate_fd(10000, 5, 2), 10000 * (1 + 0.05) ** 2, places=6)

    def test_rd(self):
        val = calculate_rd(1000, 6, 1)
        self.assertIsInstance(val, float)

    def test_retirement(self):
        self.assertIsInstance(estimate_retirement_corpus(100000, 1000, 6, 1), float)

    def test_home_loan_no_net(self):
        self.assertEqual(estimate_home_loan_eligibility(2000, 2000, 7, 15), 0.0)

    def test_credit_card(self):
        bal = calculate_credit_card_balance(1000, 24, 5, 1)
        self.assertAlmostEqual(bal, 1020 - 51, places=6)

    def test_taxable_income_cap(self):
        tax = calculate_taxable_income(30000, 10000, 10000, deduction_cap=15000)
        self.assertEqual(tax, 15000)

    def test_budget(self):
        plan = plan_budget(5000, 3000)
        self.assertAlmostEqual(plan["suggested_investment"], 600.0, places=2)

    def test_net_worth(self):
        self.assertEqual(calculate_net_worth([10000, 5000], [2000, 1000]), 12000.0)

if __name__ == "__main__":
    unittest.main()
