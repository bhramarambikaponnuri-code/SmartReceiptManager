import re


def detect_item_lines(lines):
    """
    Detect candidate item lines.

    Strategy:
    1. Ignore receipt headers and footers.
    2. Accept lines containing:
       - Item name + numbers
       - Item name only (for split OCR)
       - Numeric continuation lines
    """

    candidates = []

    ignore_words = [
        "GST",
        "CGST",
        "SGST",
        "IGST",
        "TOTAL",
        "NET",
        "AMOUNT",
        "ROUND",
        "PAYABLE",
        "PAYMENT",
        "THANK",
        "VISIT",
        "PHONE",
        "MOBILE",
        "ADDRESS",
        "CASH",
        "CARD",
        "UPI",
        "BALANCE",
        "CHANGE",
        "TENDER",
        "SUBTOTAL",
        "DISCOUNT",
        "TAX",
        "NO OF ITEMS",
        "T WT",
        "OPERATOR",
        "BILL",
        "DATE",
        "TIME",
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        upper = line.upper()

        # Ignore footer/header information
        if any(word in upper for word in ignore_words):
            continue

        # ---------------------------------------
        # Case 1
        # Name + numbers
        # Example:
        # ONION 2.475 42.00 103.95
        # ---------------------------------------

        if re.search(r"[A-Za-z]", line) and re.search(r"\d+\.\d+", line):
            candidates.append(line)
            continue

        # ---------------------------------------
        # Case 2
        # Name only
        # Example:
        # GOKARAKAYA
        # ---------------------------------------

        if re.fullmatch(r"[A-Za-z .:&()/\-]+", line):

            words = line.split()

            if 1 <= len(words) <= 5:
                candidates.append(line)

            continue

        # ---------------------------------------
        # Case 3
        # Numeric continuation line
        # Example:
        # 0.435 50.00 21.75
        # ---------------------------------------

        if re.match(r"^\d", line):

            numbers = re.findall(r"\d+\.\d+", line)

            if len(numbers) >= 2:
                candidates.append(line)

    return candidates