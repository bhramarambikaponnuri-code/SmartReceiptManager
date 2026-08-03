import re


# ---------------------------------------------------
# Valid Quantity
# ---------------------------------------------------

def is_valid_qty(value):

    try:
        qty = float(value)

        return 0 < qty <= 100

    except Exception:
        return False


# ---------------------------------------------------
# Valid Price
# ---------------------------------------------------

def is_valid_price(value):

    try:
        price = float(value)

        return 0 < price < 100000

    except Exception:
        return False


# ---------------------------------------------------
# Valid Amount
# ---------------------------------------------------

def is_valid_amount(value):

    try:
        amount = float(value)

        return 0 < amount < 100000

    except Exception:
        return False


# ---------------------------------------------------
# Valid Item Name
# ---------------------------------------------------

def is_valid_item_name(name):

    if not name:
        return False

    name = name.strip()

    if len(name) < 2:
        return False

    upper = name.upper()

    invalid_words = [
        "TOTAL",
        "NET",
        "GST",
        "CGST",
        "SGST",
        "IGST",
        "ROUND",
        "CHANGE",
        "CASH",
        "CARD",
        "UPI",
        "PAYMENT",
        "DISCOUNT",
        "AMOUNT",
        "BALANCE",
        "THANK",
        "VISIT",
        "CUSTOMER",
        "PHONE",
        "MOBILE",
        "ADDRESS",
        "DATE",
        "TIME",
        "BILL",
        "INVOICE",
        "SUBTOTAL"
    ]

    if upper in invalid_words:
        return False

    for word in invalid_words:
        if upper.startswith(word):
            return False

    # Item should contain letters
    if not re.search(r"[A-Za-z]", name):
        return False

    # Too many digits usually means OCR garbage
    digit_count = len(re.findall(r"\d", name))

    if digit_count > 4:
        return False

    return True


# ---------------------------------------------------
# Complete Item Validation
# ---------------------------------------------------

def is_valid_item(item):

    if not item:
        return False

    if not is_valid_item_name(item["Item"]):
        return False

    if item["Qty"] is not None:

        if not is_valid_qty(item["Qty"]):
            return False

    if item["Price"] is not None:

        if not is_valid_price(item["Price"]):
            return False

    if item["Amount"] is not None:

        if not is_valid_amount(item["Amount"]):
            return False

    return True