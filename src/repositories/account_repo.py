"""
Account repository: manages payment/storage accounts (cash, bank, wallet).
"""
import sqlite3
from typing import List, Optional
from src.models.entities import Account

def get_all_accounts(conn: sqlite3.Connection) -> List[Account]:
    """Retrieves all accounts."""
    rows = conn.execute("SELECT id, name, type, currency, created_at FROM accounts ORDER BY id ASC").fetchall()
    return [
        Account(
            id=r["id"],
            name=r["name"],
            type=r["type"],
            currency=r["currency"],
            created_at=r["created_at"]
        )
        for r in rows
    ]

def get_default_account(conn: sqlite3.Connection) -> Account:
    """Gets the default primary account (first account found or creates 'Cash')."""
    row = conn.execute("SELECT id, name, type, currency, created_at FROM accounts ORDER BY id ASC LIMIT 1").fetchone()
    if row:
        return Account(
            id=row["id"],
            name=row["name"],
            type=row["type"],
            currency=row["currency"],
            created_at=row["created_at"]
        )
    # If no account exists, create one
    with conn:
        cur = conn.execute("INSERT INTO accounts (name, type, currency) VALUES ('Cash', 'cash', 'USD')")
        return Account(id=cur.lastrowid, name="Cash", type="cash", currency="USD")

def create_account(conn: sqlite3.Connection, name: str, type: str, currency: str = "USD") -> int:
    """Creates a new account."""
    with conn:
        cur = conn.execute(
            "INSERT INTO accounts (name, type, currency) VALUES (?, ?, ?)",
            (name, type, currency)
        )
        return cur.lastrowid
