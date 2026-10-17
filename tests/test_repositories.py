"""
Unit and integration tests for SQLite repositories.
Uses an in-memory SQLite database for complete isolation and speed.
"""
import pytest
from src.db.connection import init_db
from src.repositories.category_repo import get_all_categories, get_category_by_id, create_category
from src.repositories.account_repo import get_all_accounts, get_default_account
from src.repositories.transaction_repo import (
    create_transaction,
    get_transaction_by_id,
    delete_transaction,
    list_transactions,
    get_monthly_totals,
    get_spending_by_category,
)
from src.repositories.budget_repo import set_category_budget, get_budgets_for_month, get_total_budget_limit_for_month
from src.repositories.settings_repo import get_user_settings, update_currency, complete_onboarding, reset_all_data

@pytest.fixture
def test_db():
    """Initializes a fresh in-memory database with tables and default seeds."""
    conn = init_db(":memory:")
    yield conn
    conn.close()

def test_categories_seeded(test_db):
    cats = get_all_categories(test_db)
    assert len(cats) >= 8
    expense_cats = get_all_categories(test_db, type_filter="expense")
    assert all(c.type == "expense" for c in expense_cats)

def test_create_and_fetch_category(test_db):
    cat_id = create_category(test_db, "Subscriptions", "📱", "#10B981", "expense")
    cat = get_category_by_id(test_db, cat_id)
    assert cat is not None
    assert cat.name == "Subscriptions"
    assert cat.icon == "📱"

def test_account_repository(test_db):
    accounts = get_all_accounts(test_db)
    assert len(accounts) >= 1
    default_acc = get_default_account(test_db)
    assert default_acc.id is not None

def test_transaction_crud_and_filters(test_db):
    acc = get_default_account(test_db)
    cats = get_all_categories(test_db, type_filter="expense")
    cat_id = cats[0].id

    # Create transaction
    txn_id = create_transaction(
        test_db,
        account_id=acc.id,
        category_id=cat_id,
        amount=1550,  # $15.50
        type="expense",
        date="2026-10-17",
        note="Campus lunch"
    )
    assert txn_id > 0

    # Fetch by ID
    txn = get_transaction_by_id(test_db, txn_id)
    assert txn is not None
    assert txn.amount == 1550
    assert txn.note == "Campus lunch"
    assert txn.category_name == cats[0].name

    # List with search filter
    search_results = list_transactions(test_db, search_query="lunch")
    assert len(search_results) == 1
    assert search_results[0].id == txn_id

    # List with unmatched search filter
    empty_results = list_transactions(test_db, search_query="nonexistent")
    assert len(empty_results) == 0

    # Monthly totals
    income_cents, expense_cents = get_monthly_totals(test_db, "2026-10")
    assert expense_cents == 1550
    assert income_cents == 0

    # Delete transaction
    deleted = delete_transaction(test_db, txn_id)
    assert deleted is True
    assert get_transaction_by_id(test_db, txn_id) is None

def test_budget_repository(test_db):
    cats = get_all_categories(test_db, type_filter="expense")
    cat_id = cats[0].id
    month = "2026-10"

    # Set budget
    set_category_budget(test_db, category_id=cat_id, month=month, limit_amount=20000)
    total_limit = get_total_budget_limit_for_month(test_db, month)
    assert total_limit == 20000

    # Add transaction in that category
    acc = get_default_account(test_db)
    create_transaction(test_db, acc.id, cat_id, amount=7500, type="expense", date="2026-10-05")

    # Verify budgets_for_month reflects spending
    budgets = get_budgets_for_month(test_db, month)
    target_budget = next(b for b in budgets if b.category_id == cat_id)
    assert target_budget.limit_amount == 20000
    assert target_budget.spent_amount == 7500

def test_settings_repository(test_db):
    settings = get_user_settings(test_db)
    assert settings.currency_code == "USD"
    assert settings.onboarding_done is False

    # Update currency
    update_currency(test_db, "EUR", "€")
    updated = get_user_settings(test_db)
    assert updated.currency_code == "EUR"
    assert updated.currency_symbol == "€"

    # Complete onboarding
    complete_onboarding(test_db, 150000)
    assert get_user_settings(test_db).onboarding_done is True
    assert get_user_settings(test_db).monthly_income == 150000

    # Reset all data
    reset_all_data(test_db)
    reset_settings = get_user_settings(test_db)
    assert reset_settings.onboarding_done is False
    assert reset_settings.monthly_income == 0
