"""
Settings repository: manages user preferences, currency, and data resets.
"""
import sqlite3
from src.models.entities import UserSettings

def get_user_settings(conn: sqlite3.Connection) -> UserSettings:
    """Retrieves user settings row."""
    row = conn.execute("SELECT id, currency_code, currency_symbol, dark_mode, onboarding_done, monthly_income FROM user_settings WHERE id = 1").fetchone()
    if not row:
        return UserSettings()
    return UserSettings(
        id=row["id"],
        currency_code=row["currency_code"],
        currency_symbol=row["currency_symbol"],
        dark_mode=bool(row["dark_mode"]),
        onboarding_done=bool(row["onboarding_done"]),
        monthly_income=int(row["monthly_income"]),
    )

def update_currency(conn: sqlite3.Connection, currency_code: str, currency_symbol: str) -> None:
    """Updates active currency code and symbol."""
    with conn:
        conn.execute(
            "UPDATE user_settings SET currency_code = ?, currency_symbol = ? WHERE id = 1",
            (currency_code, currency_symbol)
        )

def update_dark_mode(conn: sqlite3.Connection, dark_mode: bool) -> None:
    """Updates dark mode preference."""
    with conn:
        conn.execute(
            "UPDATE user_settings SET dark_mode = ? WHERE id = 1",
            (1 if dark_mode else 0,)
        )

def complete_onboarding(conn: sqlite3.Connection, monthly_income: int) -> None:
    """Marks onboarding as completed and sets estimated monthly income."""
    with conn:
        conn.execute(
            "UPDATE user_settings SET onboarding_done = 1, monthly_income = ? WHERE id = 1",
            (monthly_income,)
        )

def reset_all_data(conn: sqlite3.Connection) -> None:
    """
    Deletes all transactions, budgets, goals, and resets settings.
    Preserves categories and default accounts.
    """
    with conn:
        conn.execute("DELETE FROM transactions")
        conn.execute("DELETE FROM budgets")
        conn.execute("DELETE FROM goals")
        conn.execute(
            "UPDATE user_settings SET onboarding_done = 0, monthly_income = 0 WHERE id = 1"
        )
