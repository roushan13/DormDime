"""
Settings and Data Management View.
Provides:
1. Currency selection ($ USD, € EUR, £ GBP, ₹ INR, etc.)
2. Dark / Light mode toggle
3. Export all transactions to CSV
4. Danger Zone: Reset / Delete all user data
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from src.db.connection import get_connection
from src.repositories.settings_repo import (
    get_user_settings,
    update_currency,
    update_dark_mode,
    reset_all_data,
)
from src.repositories.transaction_repo import list_transactions
from src.utils.currency import cents_to_float

CURRENCIES = [
    ("USD", "$", "US Dollar ($)"),
    ("EUR", "€", "Euro (€)"),
    ("GBP", "£", "British Pound (£)"),
    ("INR", "₹", "Indian Rupee (₹)"),
    ("CAD", "$", "Canadian Dollar ($)"),
    ("AUD", "$", "Australian Dollar ($)"),
    ("JPY", "¥", "Japanese Yen (¥)"),
]

def render_settings_view():
    conn = get_connection()
    settings = get_user_settings(conn)

    st.markdown("### ⚙️ Preferences & Settings")

    # 1. Currency Configuration
    st.markdown("#### 💱 Currency")
    current_code = settings.currency_code
    options_labels = [c[2] for c in CURRENCIES]
    curr_map = {c[2]: (c[0], c[1]) for c in CURRENCIES}
    
    current_idx = 0
    for idx, c in enumerate(CURRENCIES):
        if c[0] == current_code:
            current_idx = idx
            break

    selected_label = st.selectbox("Display Currency", options=options_labels, index=current_idx)
    selected_code, selected_symbol = curr_map[selected_label]

    if selected_code != settings.currency_code:
        update_currency(conn, selected_code, selected_symbol)
        st.success(f"Currency updated to {selected_label}!")
        st.rerun()

    st.markdown("---")

    # 2. Export Data
    st.markdown("#### 📥 Export Data to CSV")
    st.caption("Download your full transaction history for spreadsheet analysis or backup.")

    txns = list_transactions(conn)
    if txns:
        export_records = []
        for t in txns:
            export_records.append({
                "ID": t.id,
                "Date": t.date,
                "Type": t.type.capitalize(),
                "Category": t.category_name,
                "Account": t.account_name,
                f"Amount ({selected_symbol})": cents_to_float(t.amount) if t.type == "income" else -cents_to_float(t.amount),
                "Note": t.note,
                "Created At": t.created_at,
            })
        df_export = pd.DataFrame(export_records)
        csv_data = df_export.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📄 Download Transactions CSV",
            data=csv_data,
            file_name=f"budget_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    else:
        st.info("No transactions to export yet.")

    st.markdown("---")

    # 3. Danger Zone
    st.markdown("#### ⚠️ Danger Zone")
    st.caption("Permanently delete your transaction records and monthly budget plans.")

    with st.expander("Reset Application Data", expanded=False):
        st.error("This action cannot be undone. All transactions and budgets will be permanently deleted.")
        confirm = st.checkbox("Yes, I understand and want to wipe all transaction and budget data.")
        if st.button("🗑️ Delete All My Data", type="secondary", disabled=not confirm):
            reset_all_data(conn)
            st.success("All personal data has been erased and reset to fresh state.")
            st.rerun()
