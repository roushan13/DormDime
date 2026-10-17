"""
Safe To Spend calculation pure function.
Formula:
    remaining_budget = sum(category limits) - total_spent_this_month
    days_left = days_remaining_in_month (including today)
    safe_to_spend = remaining_budget / days_left
"""

def calculate_safe_to_spend(total_budget_limit: int, total_spent_this_month: int, days_remaining: int) -> int:
    """
    Calculates the safe spending allowance for today in minor units (cents).
    
    Args:
        total_budget_limit: Total monthly budget in cents (e.g. 50000 for $500.00).
        total_spent_this_month: Total expenses logged this month in cents.
        days_remaining: Number of days left in the month, including today (must be >= 1).
        
    Returns:
        Safe to spend amount for today in integer cents. Returns 0 if overspent or days_remaining <= 0.
    """
    if days_remaining <= 0:
        return 0
    
    remaining_budget = total_budget_limit - total_spent_this_month
    
    if remaining_budget <= 0:
        return 0
    
    return remaining_budget // days_remaining

def get_budget_status(spent_cents: int, limit_cents: int) -> str:
    """
    Returns the budget status category for visual indicator:
    - 'safe': < 80% of limit
    - 'warning': 80% to 100% of limit
    - 'danger': > 100% of limit
    """
    if limit_cents <= 0:
        return "safe" if spent_cents == 0 else "danger"
    
    ratio = spent_cents / limit_cents
    if ratio > 1.0:
        return "danger"
    elif ratio >= 0.8:
        return "warning"
    return "safe"
