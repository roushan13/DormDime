"""
Unit tests for currency formatting, parsing, and conversion.
"""
from src.utils.currency import format_cents, parse_to_cents, cents_to_float

def test_format_cents_basic():
    assert format_cents(1250) == "$12.50"
    assert format_cents(0) == "$0.00"
    assert format_cents(99) == "$0.99"
    assert format_cents(5) == "$0.05"
    assert format_cents(100000) == "$1,000.00"

def test_format_cents_custom_symbol():
    assert format_cents(2500, symbol="€") == "€25.00"
    assert format_cents(50000, symbol="₹") == "₹500.00"

def test_format_cents_negative():
    assert format_cents(-1500) == "-$15.00"

def test_parse_to_cents():
    assert parse_to_cents("12.50") == 1250
    assert parse_to_cents("12") == 1200
    assert parse_to_cents("$15.99") == 1599
    assert parse_to_cents("0.05") == 5
    assert parse_to_cents(25.5) == 2550
    assert parse_to_cents(100) == 10000
    assert parse_to_cents("") == 0

def test_cents_to_float():
    assert cents_to_float(1250) == 12.50
    assert cents_to_float(500) == 5.00
    assert cents_to_float(0) == 0.0
