"""
SQLite database schema definitions and default category seed data.
"""

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- 'cash', 'bank', 'wallet'
    currency TEXT NOT NULL DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    icon TEXT NOT NULL,
    color TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('expense', 'income'))
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount INTEGER NOT NULL, -- in minor units (cents)
    type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
    date TEXT NOT NULL,      -- YYYY-MM-DD
    note TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    month TEXT NOT NULL,     -- YYYY-MM
    limit_amount INTEGER NOT NULL, -- in cents
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_id, month),
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    target INTEGER NOT NULL,  -- in cents
    saved INTEGER NOT NULL DEFAULT 0,
    deadline TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_settings (
    id INTEGER PRIMARY KEY CHECK(id = 1),
    currency_code TEXT NOT NULL DEFAULT 'USD',
    currency_symbol TEXT NOT NULL DEFAULT '$',
    dark_mode INTEGER NOT NULL DEFAULT 0,
    onboarding_done INTEGER NOT NULL DEFAULT 0,
    monthly_income INTEGER NOT NULL DEFAULT 0 -- in cents
);

CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id);
CREATE INDEX IF NOT EXISTS idx_budgets_month ON budgets(month);
"""

DEFAULT_CATEGORIES = [
    # Expenses (Tailored for College Students)
    ("Food & Dining", "🍔", "#F59E0B", "expense"),
    ("Groceries", "🛒", "#10B981", "expense"),
    ("Rent & Utilities", "🏠", "#3B82F6", "expense"),
    ("Transport", "🚌", "#6366F1", "expense"),
    ("Books & Study", "📚", "#8B5CF6", "expense"),
    ("Entertainment", "🎮", "#EC4899", "expense"),
    ("Personal Care", "🧴", "#14B8A6", "expense"),
    ("Other Expense", "📦", "#64748B", "expense"),
    # Incomes
    ("Allowance", "👨‍👩‍👧", "#10B981", "income"),
    ("Part-Time Job", "💼", "#3B82F6", "income"),
    ("Scholarship", "🎓", "#8B5CF6", "income"),
    ("Other Income", "💵", "#059669", "income"),
]
