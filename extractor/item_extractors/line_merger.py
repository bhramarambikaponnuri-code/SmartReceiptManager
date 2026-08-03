import re


def is_item_name(line):
    """
    Returns True if the line looks like an item name.
    """

    line = line.strip()

    if not line:
        return False

    # Must contain letters
    if not re.search(r"[A-Za-z]", line):
        return False

    # Should not already contain price values
    if re.search(r"\d+\.\d{2}", line):
        return False

    # Ignore totals and headers
    blocked = [
        "TOTAL",
        "GST",
        "CGST",
        "SGST",
        "ROUND",
        "AMOUNT",
        "PRICE",
        "RATE",
        "QTY",
        "WT",
        "ITEM",
        "THANK",
        "CASH",
        "CARD"
    ]

    upper = line.upper()

    if any(word in upper for word in blocked):
        return False

    return True


def is_numeric_line(line):
    """
    Returns True if the line contains only numeric values
    like Qty Price Amount.
    """

    line = line.strip()

    if not line:
        return False

    # Starts with a number
    if not re.match(r"^\d", line):
        return False

    numbers = re.findall(r"\d+\.\d{2,3}", line)

    return len(numbers) >= 2


def merge_item_lines(lines):
    """
    Merge OCR outputs like:

    GOKARAKAYA
    0.435 50.00 21.75

    into

    GOKARAKAYA 0.435 50.00 21.75
    """

    merged = []

    i = 0

    while i < len(lines):

        current = lines[i].strip()

        if i + 1 < len(lines):

            nxt = lines[i + 1].strip()

            if is_item_name(current) and is_numeric_line(nxt):

                merged.append(current + " " + nxt)

                i += 2
                continue

        merged.append(current)

        i += 1

    return merged