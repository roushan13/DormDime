"""
Currency utilities.
Monetary values are treated as integer cents internally to avoid floating point inaccuracies.
"""
import re

def format_cents(cents: int, symbol: str = "$") -> str:
    """
    Formats integer cents into human-readable currency.
    Example: 1250 -> "$12.50", -500 -> "-$5.00"
    """
    is_negative = cents < 0
    abs_cents = abs(cents)
    dollars = abs_cents // 100
    remainder = abs_cents % 100
    formatted = f"{dollars:,}.{remainder:02d}"
    if is_negative:
        return f"-{symbol}{formatted}"
    return f"{symbol}{formatted}"

def parse_to_cents(amount_input: str | float | int) -> int:
    """
    Parses user input string or number into integer cents.
    Example: '12.50' -> 1250, '12' -> 1200, 15.75 -> 1575
    """
    if isinstance(amount_input, (int, float)):
        # Round to 2 decimal places before converting to integer cents
        return int(round(float(amount_input) * 100))
    
    clean_str = re.sub(r"[^\d.-]", "", str(amount_input).strip())
    if not clean_str or clean_str == "-":
        return 0
    
    val = float(clean_str)
    return int(round(val * 100))

def cents_to_float(cents: int) -> float:
    """Converts integer cents to float for chart inputs."""
    return round(cents / 100.0, 2)
