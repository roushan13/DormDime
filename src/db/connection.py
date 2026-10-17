"""
Database connection management and initialization.
Supports file-based SQLite database and in-memory databases for tests.
"""
import sqlite3
import os
from typing import Optional
from src.db.schema import SCHEMA_SQL, DEFAULT_CATEGORIES

DEFAULT_DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "budget.db")

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Returns a configured SQLite connection with row_factory enabled.
    """
    path = db_path if db_path is not None else DEFAULT_DB_FILE
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Initializes tables, default settings, and seeds initial categories if not already present.
    """
    conn = get_connection(db_path)
    with conn:
        conn.executescript(SCHEMA_SQL)
        
        # Ensure default user settings row (id=1)
        cur = conn.execute("SELECT id FROM user_settings WHERE id = 1")
        if not cur.fetchone():
            conn.execute(
                "INSERT INTO user_settings (id, currency_code, currency_symbol, dark_mode, onboarding_done, monthly_income) VALUES (1, 'USD', '$', 0, 0, 0)"
            )
            
        # Ensure default accounts exist
        cur = conn.execute("SELECT COUNT(*) as count FROM accounts")
        if cur.fetchone()["count"] == 0:
            conn.execute("INSERT INTO accounts (name, type, currency) VALUES ('Cash', 'cash', 'USD')")
            conn.execute("INSERT INTO accounts (name, type, currency) VALUES ('Bank Account', 'bank', 'USD')")
            
        # Seed categories if table is empty
        cur = conn.execute("SELECT COUNT(*) as count FROM categories")
        if cur.fetchone()["count"] == 0:
            conn.executemany(
                "INSERT INTO categories (name, icon, color, type) VALUES (?, ?, ?, ?)",
                DEFAULT_CATEGORIES
            )
            
    return conn
