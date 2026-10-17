"""
Unit tests for safe to spend calculation and budget status rules.
"""
from src.utils.safe_to_spend import calculate_safe_to_spend, get_budget_status

def test_safe_to_spend_standard_case():
    # Budget $500 (50,000 cents), Spent $200 (20,000 cents), 15 days remaining
    # Remaining: $300 (30,000 cents) / 15 = 2,000 cents ($20.00 / day)
    result = calculate_safe_to_spend(50000, 20000, 15)
    assert result == 2000

def test_safe_to_spend_overspent():
    # Spent more than limit -> must return 0, not negative
    result = calculate_safe_to_spend(30000, 35000, 10)
    assert result == 0

def test_safe_to_spend_exact_budget():
    # Exactly spent all budget -> returns 0
    result = calculate_safe_to_spend(40000, 40000, 5)
    assert result == 0

def test_safe_to_spend_last_day_of_month():
    # 1 day remaining -> full remaining budget can be spent today
    result = calculate_safe_to_spend(50000, 40000, 1)
    assert result == 10000

def test_safe_to_spend_zero_or_negative_days():
    # Defensive check against non-positive days
    assert calculate_safe_to_spend(50000, 20000, 0) == 0
    assert calculate_safe_to_spend(50000, 20000, -2) == 0

def test_budget_status_colors():
    # Safe (< 80%)
    assert get_budget_status(7000, 10000) == "safe"
    # Warning (80% - 100%)
    assert get_budget_status(8000, 10000) == "warning"
    assert get_budget_status(9500, 10000) == "warning"
    assert get_budget_status(10000, 10000) == "warning"
    # Danger (> 100%)
    assert get_budget_status(10001, 10000) == "danger"
    assert get_budget_status(15000, 10000) == "danger"
