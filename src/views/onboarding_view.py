"""
Onboarding View for First-Time Users.
Sets up estimated monthly income, fixed costs, and initial category targets.
"""
import streamlit as st
from src.db.connection import get_connection
from src.repositories.settings_repo import get_user_settings, complete_onboarding
from src.repositories.category_repo import get_all_categories
from src.repositories.budget_repo import set_category_budget
from src.utils.currency import parse_to_cents
from src.utils.date_helpers import get_current_month_str

def render_onboarding_view():
    conn = get_connection()
    settings = get_user_settings(conn)
    currency_symbol = settings.currency_symbol

    st.markdown(
        f"""
        <div class="metric-card" style="border-left: 6px solid #3B82F6;">
            <h2 style="margin: 0; font-size: 1.5rem;">🎓 Welcome to Student Budget Tracker!</h2>
            <p style="color: #64748B; margin-top: 6px; margin-bottom: 0;">
                Take 30 seconds to set your monthly targets so we can calculate your <b>Safe to Spend Today</b> amount.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("onboarding_form"):
        st.markdown("#### 1. Irregular Income & Allowance")
        income_dollars = st.number_input(
            f"Expected Monthly Inflow ({currency_symbol}) — allowance, part-time job, scholarship",
            min_value=0.0,
            value=800.0,
            step=50.0,
        )

        st.markdown("#### 2. Initial Category Limits")
        st.caption("Allocate roughly how much you plan to spend this month:")

        col1, col2 = st.columns(2)
        with col1:
            food_limit = st.number_input(f"🍔 Food & Dining ({currency_symbol})", min_value=0.0, value=250.0, step=25.0)
            groceries_limit = st.number_input(f"🛒 Groceries ({currency_symbol})", min_value=0.0, value=150.0, step=25.0)
            rent_limit = st.number_input(f"🏠 Rent & Utilities ({currency_symbol})", min_value=0.0, value=200.0, step=50.0)
        with col2:
            transport_limit = st.number_input(f"🚌 Transport ({currency_symbol})", min_value=0.0, value=50.0, step=10.0)
            books_limit = st.number_input(f"📚 Books & Study ({currency_symbol})", min_value=0.0, value=50.0, step=10.0)
            fun_limit = st.number_input(f"🎮 Entertainment ({currency_symbol})", min_value=0.0, value=50.0, step=10.0)

        col_save, col_skip = st.columns([2, 1])
        with col_save:
            submitted = st.form_submit_button("🚀 Finish Setup & Open Dashboard", type="primary", use_container_width=True)
        with col_skip:
            skipped = st.form_submit_button("⏩ Skip for Now", use_container_width=True)

        if submitted:
            income_cents = parse_to_cents(income_dollars)
            complete_onboarding(conn, income_cents)

            # Map category allocations to current month
            current_month = get_current_month_str()
            cats = get_all_categories(conn, type_filter="expense")
            name_to_id = {c.name: c.id for c in cats}

            allocations = [
                ("Food & Dining", food_limit),
                ("Groceries", groceries_limit),
                ("Rent & Utilities", rent_limit),
                ("Transport", transport_limit),
                ("Books & Study", books_limit),
                ("Entertainment", fun_limit),
            ]
            for cat_name, limit_val in allocations:
                if cat_name in name_to_id:
                    set_category_budget(conn, name_to_id[cat_name], current_month, parse_to_cents(limit_val))

            st.success("🎉 Setup completed! Redirecting to your dashboard...")
            st.rerun()

        elif skipped:
            complete_onboarding(conn, parse_to_cents(income_dollars))
            st.rerun()
