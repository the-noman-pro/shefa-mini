"""
Card checks for the simulated top-up. Pure functions, no Django, so they are easy to test.

The same rules live in the frontend (frontend/src/lib/card.js) for live feedback; the server
checks again because the browser cannot be trusted.
"""

import re
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

MIN_TOP_UP = Decimal("10.00")
MAX_TOP_UP = Decimal("10000.00")

# Always declined by the simulated processor.
DECLINED_TEST_CARD = "4000000000000002"

# A short list of Mada-style BIN prefixes. Checked before Visa/Mastercard because they overlap.
MADA_PREFIXES = (
    "440647", "440795", "446404", "457865", "457997", "474491", "588845", "588846",
    "588847", "588848", "588849", "588850", "588851", "588982", "589005", "604906",
    "636120", "968201", "968202", "968203", "968204", "968205", "968206", "968207",
    "968208", "968209", "968210", "968211",
)  # fmt: skip


def digits_only(value):
    return re.sub(r"\D", "", value or "")


def luhn_valid(number):
    if not number.isdigit():
        return False
    total = 0
    for index, char in enumerate(reversed(number)):
        digit = int(char)
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def detect_brand(number):
    """Return "mada", "visa", "mastercard", "amex" or "" from the number's prefix."""
    if not number:
        return ""
    if number.startswith(MADA_PREFIXES):
        return "mada"
    if number.startswith("4"):
        return "visa"
    if number[:2] in {"34", "37"}:
        return "amex"
    if len(number) >= 2 and 51 <= int(number[:2]) <= 55:
        return "mastercard"
    if len(number) >= 4 and 2221 <= int(number[:4]) <= 2720:
        return "mastercard"
    return ""


BRAND_LABELS = {"visa": "Visa", "mastercard": "Mastercard", "mada": "Mada", "amex": "Amex"}


def validate_card_number(raw):
    """Return (digits, brand, error). error is "" when the number is acceptable."""
    number = digits_only(raw)
    if not number:
        return number, "", "Enter the card number."
    if not 13 <= len(number) <= 19:
        return number, "", "A card number has 13 to 19 digits."
    brand = detect_brand(number)
    if not brand:
        return number, "", "We accept Visa, Mastercard, Mada and Amex."
    if brand == "amex" and len(number) != 15:
        return number, brand, "An Amex number has 15 digits."
    if not luhn_valid(number):
        return number, brand, "This card number is not valid. Check the digits."
    return number, brand, ""


def parse_expiry(raw, today=None):
    """Return (month, year, error) for an "MM/YY" value; the card works until the month's end."""
    today = today or date.today()
    match = re.fullmatch(r"\s*(\d{2})\s*/\s*(\d{2})\s*", raw or "")
    if not match:
        return None, None, "Use the format MM/YY."
    month, year = int(match.group(1)), 2000 + int(match.group(2))
    if not 1 <= month <= 12:
        return None, None, "The month must be between 01 and 12."
    if (year, month) < (today.year, today.month):
        return month, year, "This card has expired."
    if year > today.year + 20:
        return month, year, "Check the expiry year."
    return month, year, ""


def validate_cvv(raw, brand):
    expected = 4 if brand == "amex" else 3
    if not re.fullmatch(rf"\d{{{expected}}}", raw or ""):
        return f"The security code is {expected} digits."
    return ""


def parse_amount(raw, minimum=MIN_TOP_UP, maximum=MAX_TOP_UP):
    """Return (Decimal amount, error). Accepts up to two decimal places."""
    try:
        amount = Decimal(str(raw).strip())
    except (InvalidOperation, ValueError):
        return None, "Enter an amount in SAR."
    if not amount.is_finite():
        return None, "Enter an amount in SAR."
    if amount != amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP):
        return None, "Use at most two decimal places."
    if amount < minimum:
        return None, f"The minimum is {minimum:,.0f} SAR."
    if amount > maximum:
        return None, f"The maximum is {maximum:,.0f} SAR."
    return amount.quantize(Decimal("0.01")), ""
