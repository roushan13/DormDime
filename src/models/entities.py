"""
Domain models for the budget tracker.
All monetary amounts are stored as integers (minor units / cents) to prevent precision loss.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Account:
    id: Optional[int]
    name: str
    type: str  # 'cash', 'bank', 'wallet'
    currency: str = "USD"
    created_at: Optional[str] = None

@dataclass
class Category:
    id: Optional[int]
    name: str
    icon: str
    color: str
    type: str  # 'expense' or 'income'

@dataclass
class Transaction:
    id: Optional[int]
    account_id: int
    category_id: int
    amount: int  # integer in minor units (cents)
    type: str    # 'expense' or 'income'
    date: str    # 'YYYY-MM-DD'
    note: str = ""
    created_at: Optional[str] = None
    # Joined fields for convenient UI display
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    category_color: Optional[str] = None
    account_name: Optional[str] = None

@dataclass
class Budget:
    id: Optional[int]
    category_id: int
    month: str       # 'YYYY-MM'
    limit_amount: int  # integer in minor units (cents)
    created_at: Optional[str] = None
    # Joined fields for UI
    category_name: Optional[str] = None
    category_icon: Optional[str] = None
    category_color: Optional[str] = None
    spent_amount: int = 0

@dataclass
class UserSettings:
    id: int = 1
    currency_code: str = "USD"
    currency_symbol: str = "$"
    dark_mode: bool = False
    onboarding_done: bool = False
    monthly_income: int = 0  # cents
