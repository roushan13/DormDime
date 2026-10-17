# 💸 Student Budget Tracker (Python + Streamlit)

A fast, simple, offline-first budget tracker designed specifically for college students with irregular income (allowance, part-time jobs, scholarships) and frequent small expenses. Logging an expense takes under 5 seconds!

---

## 🌟 Key Features

1. **Safe to Spend Today**: A real-time calculated hero allowance based on remaining category budgets divided by days remaining in the month.
2. **Category Progress Bars**: Immediate visual feedback (🟢 Safe `<80%`, 🟡 Warning `80-100%`, 🔴 Alert `>100%`).
3. **< 5s Transaction Logging**: Fast numeric keypad / quick-addition buttons (`+$1`, `+$5`, `+$10`, `+$20`, `+$50`), category selector chips, and 1-tap save.
4. **Searchable History**: Filter by search keywords, category, income/expense type, and flexible date ranges.
5. **Budgets**: Set and adjust monthly limits per category with immediate comparison against actual spending.
6. **Visual Insights**: Interactive Plotly donut chart for category breakdown and 6-month income vs. expense trend analysis.
7. **Settings & Portability**: Currency selector (`$`, `€`, `£`, `₹`, etc.), 1-click CSV export download, and safe data wipe.
8. **Onboarding**: Simple setup for monthly inflow and category targets.

---

## 🛠️ Architecture

- **UI Layer**: Streamlit centered, mobile-first responsive view with custom card CSS tokens.
- **Repository Layer**: SQLite database access decoupled from UI code (`src/repositories/`).
- **Data Integrity**: All monetary values are strictly stored as **integers in minor units (cents)** to eliminate floating-point calculation errors.
- **Business Logic**: Pure functions (`calculate_safe_to_spend`, `format_cents`, `parse_to_cents`) tested with 100% unit test coverage.

---

## 🚀 Quick Start

### 1. Activate Environment & Install Dependencies
```bash
# If using the project's virtual environment:
.\.venv\Scripts\Activate.ps1

# Install requirements (if not already installed)
pip install -r budget-tracker-py/requirements.txt
```

### 2. Run the Application
```bash
cd budget-tracker-py
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 3. Run Automated Tests
```bash
cd budget-tracker-py
pytest tests -v
```
