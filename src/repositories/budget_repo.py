"""
Budget repository: manages monthly spending limits and compares actual vs budgeted spending.
"""
import sqlite3
from typing import List, Optional
from src.models.entities import Budget

def set_category_budget(conn: sqlite3.Connection, category_id: int, month: str, limit_amount: int) -> None:
    """
    Sets or updates the spending limit for a category in a specific month (YYYY-MM).
    """
    with conn:
        conn.execute(
            """
            INSERT INTO budgets (category_id, month, limit_amount)
            VALUES (?, ?, ?)
            ON CONFLICT(category_id, month) DO UPDATE SET limit_amount = excluded.limit_amount
            """,
            (category_id, month, limit_amount)
        )

def get_budgets_for_month(conn: sqlite3.Connection, month: str) -> List[Budget]:
    """
    Retrieves all expense categories, their budget limits for the month, and total spent.
    """
    query = """
        SELECT c.id as category_id, c.name as category_name, c.icon as category_icon, c.color as category_color,
               COALESCE(b.id, NULL) as budget_id,
               COALESCE(b.limit_amount, 0) as limit_amount,
               COALESCE(SUM(t.amount), 0) as spent_amount
        FROM categories c
        LEFT JOIN budgets b ON b.category_id = c.id AND b.month = ?
        LEFT JOIN transactions t ON t.category_id = c.id AND t.type = 'expense' AND strftime('%Y-%m', t.date) = ?
        WHERE c.type = 'expense'
        GROUP BY c.id, c.name, c.icon, c.color, b.id, b.limit_amount
        ORDER BY limit_amount DESC, spent_amount DESC
    """
    rows = conn.execute(query, (month, month)).fetchall()
    return [
        Budget(
            id=r["budget_id"],
            category_id=r["category_id"],
            month=month,
            limit_amount=int(r["limit_amount"]),
            category_name=r["category_name"],
            category_icon=r["category_icon"],
            category_color=r["category_color"],
            spent_amount=int(r["spent_amount"]),
        )
        for r in rows
    ]

def get_total_budget_limit_for_month(conn: sqlite3.Connection, month: str) -> int:
    """Calculates sum of all category budget limits for a given month."""
    query = "SELECT SUM(limit_amount) as total_limit FROM budgets WHERE month = ?"
    row = conn.execute(query, (month,)).fetchone()
    return int(row["total_limit"] or 0)
