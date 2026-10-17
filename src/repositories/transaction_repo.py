"""
Transaction repository: handles transaction CRUD, searching, filtering, and aggregations.
"""
import sqlite3
from typing import List, Optional, Tuple, Dict
from src.models.entities import Transaction

def create_transaction(
    conn: sqlite3.Connection,
    account_id: int,
    category_id: int,
    amount: int,
    type: str,
    date: str,
    note: str = ""
) -> int:
    """Inserts a new transaction with amount stored in minor units (cents)."""
    with conn:
        cur = conn.execute(
            """
            INSERT INTO transactions (account_id, category_id, amount, type, date, note)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (account_id, category_id, amount, type, date, note.strip())
        )
        return cur.lastrowid

def get_transaction_by_id(conn: sqlite3.Connection, txn_id: int) -> Optional[Transaction]:
    """Retrieves a single transaction by ID with joined category and account details."""
    query = """
        SELECT t.id, t.account_id, t.category_id, t.amount, t.type, t.date, t.note, t.created_at,
               c.name as category_name, c.icon as category_icon, c.color as category_color,
               a.name as account_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN accounts a ON t.account_id = a.id
        WHERE t.id = ?
    """
    row = conn.execute(query, (txn_id,)).fetchone()
    if not row:
        return None
    return Transaction(
        id=row["id"],
        account_id=row["account_id"],
        category_id=row["category_id"],
        amount=row["amount"],
        type=row["type"],
        date=row["date"],
        note=row["note"],
        created_at=row["created_at"],
        category_name=row["category_name"],
        category_icon=row["category_icon"],
        category_color=row["category_color"],
        account_name=row["account_name"],
    )

def delete_transaction(conn: sqlite3.Connection, txn_id: int) -> bool:
    """Deletes a transaction by ID."""
    with conn:
        cur = conn.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
        return cur.rowcount > 0

def list_transactions(
    conn: sqlite3.Connection,
    search_query: Optional[str] = None,
    category_id: Optional[int] = None,
    type_filter: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[Transaction]:
    """
    Retrieves transactions with dynamic filters for search, category, type, and date range.
    """
    conditions = []
    params = []

    if search_query:
        query_pattern = f"%{search_query.strip()}%"
        conditions.append("(t.note LIKE ? OR c.name LIKE ?)")
        params.extend([query_pattern, query_pattern])

    if category_id:
        conditions.append("t.category_id = ?")
        params.append(category_id)

    if type_filter and type_filter != "all":
        conditions.append("t.type = ?")
        params.append(type_filter)

    if start_date:
        conditions.append("t.date >= ?")
        params.append(start_date)

    if end_date:
        conditions.append("t.date <= ?")
        params.append(end_date)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    limit_clause = f"LIMIT {int(limit)}" if limit else ""

    sql = f"""
        SELECT t.id, t.account_id, t.category_id, t.amount, t.type, t.date, t.note, t.created_at,
               c.name as category_name, c.icon as category_icon, c.color as category_color,
               a.name as account_name
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
        LEFT JOIN accounts a ON t.account_id = a.id
        {where_clause}
        ORDER BY t.date DESC, t.id DESC
        {limit_clause}
    """
    rows = conn.execute(sql, params).fetchall()
    return [
        Transaction(
            id=r["id"],
            account_id=r["account_id"],
            category_id=r["category_id"],
            amount=r["amount"],
            type=r["type"],
            date=r["date"],
            note=r["note"],
            created_at=r["created_at"],
            category_name=r["category_name"],
            category_icon=r["category_icon"],
            category_color=r["category_color"],
            account_name=r["account_name"],
        )
        for r in rows
    ]

def get_monthly_totals(conn: sqlite3.Connection, month: str) -> Tuple[int, int]:
    """
    Returns (total_income_cents, total_expense_cents) for a given month 'YYYY-MM'.
    """
    query = """
        SELECT
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
        FROM transactions
        WHERE strftime('%Y-%m', date) = ?
    """
    row = conn.execute(query, (month,)).fetchone()
    total_income = row["total_income"] or 0
    total_expense = row["total_expense"] or 0
    return int(total_income), int(total_expense)

def get_spending_by_category(conn: sqlite3.Connection, month: str) -> List[Dict]:
    """
    Returns aggregated expenses grouped by category for a given month 'YYYY-MM'.
    """
    query = """
        SELECT c.id as category_id, c.name as category_name, c.icon, c.color,
               SUM(t.amount) as total_spent
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE t.type = 'expense' AND strftime('%Y-%m', t.date) = ?
        GROUP BY c.id, c.name, c.icon, c.color
        ORDER BY total_spent DESC
    """
    rows = conn.execute(query, (month,)).fetchall()
    return [
        {
            "category_id": r["category_id"],
            "category_name": r["category_name"],
            "icon": r["icon"],
            "color": r["color"],
            "total_spent": int(r["total_spent"]),
        }
        for r in rows
    ]

def get_monthly_trend(conn: sqlite3.Connection, limit_months: int = 6) -> List[Dict]:
    """
    Returns monthly expense and income trend data for the past N months.
    """
    query = """
        SELECT
            strftime('%Y-%m', date) as month,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income
        FROM transactions
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month DESC
        LIMIT ?
    """
    rows = conn.execute(query, (limit_months,)).fetchall()
    # Return chronologically ascending for charts
    results = [
        {
            "month": r["month"],
            "total_expense": int(r["total_expense"] or 0),
            "total_income": int(r["total_income"] or 0),
        }
        for r in rows
    ]
    results.reverse()
    return results
