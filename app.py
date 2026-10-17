"""
Student Budget Tracker — Main Entrypoint.
Provides top-level navigation, theme injection, database initialization, and view rendering.
"""
import sys
import os

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
from src.db.connection import init_db, get_connection
from src.repositories.settings_repo import get_user_settings
from src.theme.styles import inject_theme
from src.views.dashboard_view import render_dashboard_view
from src.views.add_view import render_add_view
from src.views.transactions_view import render_transactions_view
from src.views.budgets_view import render_budgets_view
from src.views.insights_view import render_insights_view
from src.views.settings_view import render_settings_view
from src.views.onboarding_view import render_onboarding_view

# Page Configuration (Mobile-first centered layout)
st.set_page_config(
    page_title="Student Budget Tracker",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize database schema and default seeds
init_db()

# Inject minimal modern CSS
inject_theme()

# Top Header
st.title("💸 Student Budget Tracker")

conn = get_connection()
settings = get_user_settings(conn)

# If first-time user hasn't completed onboarding, present it prominently
if not settings.onboarding_done:
    render_onboarding_view()
    st.markdown("---")

# Navigation Tabs (representing bottom tabs in mobile design)
tab_home, tab_add, tab_txns, tab_budgets, tab_insights, tab_settings = st.tabs([
    "🏠 Home",
    "➕ Add",
    "📋 Transactions",
    "🎯 Budgets",
    "📊 Insights",
    "⚙️ Settings",
])

with tab_home:
    render_dashboard_view()

with tab_add:
    render_add_view()

with tab_txns:
    render_transactions_view()

with tab_budgets:
    render_budgets_view()

with tab_insights:
    render_insights_view()

with tab_settings:
    render_settings_view()
