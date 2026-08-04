import re

ITEM_BAD_WORDS = {
    "GST",
    "GSTIN",
    "DATE",
    "TIME",
    "TOKEN",
    "CASHIER",
    "TABLE",
    "NAME",
    "PHONE",
    "MOBILE",
    "ADDRESS",
    "INVOICE",
    "RECEIPT",
    "THANK",
    "VISIT",
    "FSSAI",
    "CGST",
    "SGST",
    "IGST",
    "DISCOUNT",
    "ROUND OFF",
    "TOTAL QTY",
    "TATAL QTY",
    "SUB TOTAL",
    "SUB TATAL",
    "GRAND TOTAL"
}

def is_bad_item_line(line):
    """
    Returns True if the line should never be treated as an item.
    """

    upper = line.upper()

    return any(word in upper for word in ITEM_BAD_WORDS)


import re


def clean_ocr_line(line):
    """
    Fix common OCR mistakes.
    """

    line = line.upper()

    # decimal comma
    line = re.sub(r'(\d),(\d{2})\b', r'\1.\2', line)

    # thousands comma
    line = re.sub(r'(\d),(\d{3})\b', r'\1\2', line)

    # Remove comma after quantity like "1," -> "1"
    line = re.sub(r'(\d),\s', r'\1 ', line)

    line = re.sub(
        r"\b1\s*/\s*2\s+SOUP\b",
        "",
        line,
        flags=re.IGNORECASE
    )

    line = line.replace("D0", "00")
    line = line.replace("DO", "00")
    line = line.replace("Q0", "00")
    line = line.replace("O0", "00")
    line = line.replace("[Q", "00")
    line = line.replace("I0", "10")
    line = line.replace(",000", "1.000")
    line = line.replace(" O00", "1.000")
    line = line.replace(",OQ0", "1.000")
    line = line.replace(",QQQ", "1.000")

    # Remove serving-size words
    line = re.sub(
        r"\b(1/2|HALF|FULL|QUARTER)\s+[A-Z]+\b",
        "",
        line,
        flags=re.IGNORECASE
    )

    # Remove an extra trailing quantity left after serving-size removal

    line = re.sub(r"\s+\d+$", "", line)

    line = re.sub(r"\s+", " ", line)

    return line.strip()


def looks_like_item(line):

    upper = line.upper()

    if upper.startswith(("H.NO", "NO.", "PLOT", "SURVEY")):
        return False

    reject_words = [

        "GST",
        "GSTIN",
        "FSSAI",
        "SURVEY",
        "BLOCK",
        "PLOT",
        "TOKEN",
        "BILL NO",
        "CASHIER",
        "DATE",
        "TIME",
        "SUB TOTAL",
        "GRAND TOTAL",
        "TOTAL QTY",
        "PHONE",
        "TELANGANA",
        "HYDERABAD",
        "RANGAREDDI",
        "WELCOME",
        "THANK",
        "VISIT"

    ]

    reject_words += [

        "VAT",
        "SERVICE",
        "SERVICE CHARGE",
        "SERVICE TAX",
        "CGST",
        "SGST",
        "CESS",
        "DISCOUNT",
        "SUBTOTAL",
        "TOTAL QUANTITY",
        "ROUND OFF"

    ]

    if any(word in upper for word in reject_words):
        return False

    # Address lines
    if upper.startswith(("H.NO", "NO.", "PLOT", "SURVEY")):
        return False

    # PIN codes like 500079
    if re.search(r"\b\d{6}\b", line):
        return False

    if len(line) < 4:
        return False

    if not any(c.isalpha() for c in line):
        return False

    if not any(c.isdigit() for c in line):
        return False

    return True


def parse_item(line):

    line = clean_ocr_line(line)

    print("AFTER CLEAN:", line)

    lower = line.lower()

    if (
        "total qty" in lower or
        "tatal qty" in lower or
        "sub total" in lower or
        "sub tatal" in lower or
        "grand total" in lower
    ):
        return None

    if re.search(
        r"(ROAD|RD|STREET|LANE|NAGAR|COLONY|PLOT|SURVEY|BLOCK|HYDERABAD|TELANGANA)",
        line.upper()
    ):
        return None

    if is_bad_item_line(line):
        return None

    if not looks_like_item(line):
        return None

    numbers = re.findall(r"\d+\.\d+|\d+", line)
    print("VALUES:", numbers)

    if len(numbers) == 4:
        numbers = numbers[:-1]

    if len(numbers) < 2:
        return None

    values = [float(x) for x in numbers]

    item_name = re.sub(r"\d.*", "", line).strip()

    item_name = re.sub(r"\s+", " ", item_name)

    if len(item_name) < 2:
        return None

    qty = None
    price = None
    amount = None

    # -------------------------------
    # Pattern 1
    # Qty Price Amount
    # -------------------------------

    if len(values) >= 3:

        q = values[-3]
        p = values[-2]
        a = values[-1]

        if q <= 20 and abs(q * p - a) <= 2:
            qty = q
            price = p
            amount = a

    # -------------------------------
    # Pattern 2
    # Price Amount
    # -------------------------------

    if qty is None and len(values) >= 2:

        p = values[-2]
        a = values[-1]

        if abs(p - a) <= 2:
            qty = 1
            price = p
            amount = a

    # -------------------------------
    # Pattern 3
    # Qty Price
    # -------------------------------

    if qty is None and len(values) >= 2:

        q = values[-2]
        p = values[-1]

        if q <= 20:
            qty = q
            price = p
            amount = q * p

    if qty is None or qty > 20:
        return None

    if qty == 0:
        return None

    if price > amount and amount > 0:
        return None

    return {

        "Qty": qty,
        "Item": item_name.title(),
        "Price": round(price, 2),
        "Amount": round(amount, 2)

    }