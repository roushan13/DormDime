"""
Date helpers for month boundaries and days-remaining calculations.
"""
import calendar
from datetime import date, datetime
from typing import Optional

def get_today_date() -> date:
    """Returns today's date."""
    return date.today()

def get_today_str() -> str:
    """Returns today in 'YYYY-MM-DD' format."""
    return get_today_date().strftime("%Y-%m-%d")

def get_current_month_str() -> str:
    """Returns current month in 'YYYY-MM' format."""
    return get_today_date().strftime("%Y-%m")

def days_in_month(year: int, month: int) -> int:
    """Returns total number of days in the specified month."""
    _, num_days = calendar.monthrange(year, month)
    return num_days

def get_days_remaining_in_month(target_date: Optional[date] = None) -> int:
    """
    Returns days remaining in the month including the target date (today).
    Example: On October 17th, with 31 days in October:
    31 - 17 + 1 = 15 days remaining.
    """
    d = target_date if target_date is not None else get_today_date()
    total_days = days_in_month(d.year, d.month)
    return max(1, total_days - d.day + 1)
