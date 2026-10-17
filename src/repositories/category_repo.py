"""
Category repository: manages category data retrieval and creation.
"""
import sqlite3
from typing import Optional, List
from src.models.entities import Category

def get_all_categories(conn: sqlite3.Connection, type_filter: Optional[str] = None) -> List[Category]:
    """
    Retrieves all categories, optionally filtered by type ('expense' or 'income').
    """
    if type_filter:
        query = "SELECT id, name, icon, color, type FROM categories WHERE type = ? ORDER BY id ASC"
        rows = conn.execute(query, (type_filter,)).fetchall()
    else:
        query = "SELECT id, name, icon, color, type FROM categories ORDER BY type DESC, id ASC"
        rows = conn.execute(query).fetchall()
        
    return [
        Category(
            id=r["id"],
            name=r["name"],
            icon=r["icon"],
            color=r["color"],
            type=r["type"],
        )
        for r in rows
    ]

def get_category_by_id(conn: sqlite3.Connection, category_id: int) -> Optional[Category]:
    """Retrieves a single category by primary key."""
    row = conn.execute(
        "SELECT id, name, icon, color, type FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()
    if not row:
        return None
    return Category(
        id=row["id"],
        name=row["name"],
        icon=row["icon"],
        color=row["color"],
        type=row["type"],
    )

def create_category(conn: sqlite3.Connection, name: str, icon: str, color: str, type: str) -> int:
    """Creates a new category and returns its ID."""
    with conn:
        cur = conn.execute(
            "INSERT INTO categories (name, icon, color, type) VALUES (?, ?, ?, ?)",
            (name, icon, color, type)
        )
        return cur.lastrowid
