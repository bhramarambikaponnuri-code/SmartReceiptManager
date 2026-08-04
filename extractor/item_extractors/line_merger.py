import re


def is_item_name(line):
    """
    Returns True if line looks like an item description.
    """

    line = line.strip()

    if not line:
        return False

    # Must contain alphabets
    if not re.search(r"[A-Za-z]", line):
        return False

    # Ignore obvious non-item headers
    blocked = [
        "TOTAL",
        "GST",
        "CGST",
        "SGST",
        "IGST",
        "ROUND",
        "DISCOUNT",
        "AMOUNT",
        "PRICE",
        "RATE",
        "QTY",
        "QUANTITY",
        "UNIT",
        "ITEM",
        "THANK",
        "WELCOME",
        "CASH",
        "CARD",
        "DATE",
        "INVOICE",
        "BILL"
    ]

    upper = line.upper()

    if any(word in upper for word in blocked):
        return False

    return True


def is_amount_only(line):
    """
    Returns True if the line contains only one amount.

    Example:
        100.00
        1,500.00
    """

    line = line.strip()

    return bool(
        re.fullmatch(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})?", line)
    )


def merge_item_lines(lines):
    """
    Merge OCR-split item lines.

    Handles:

    ITEM
    Qty Price Amount

    ITEM Qty Price
    Amount

    ITEM Qty
    Price
    Amount
    """

    merged = []

    i = 0

    while i < len(lines):

        current = lines[i].strip()

        # -------------------------
        # Case 1
        # Current line contains text
        # Next line is only amount
        # -------------------------

        if (
            i + 1 < len(lines)
            and re.search(r"[A-Za-z]", current)
            and is_amount_only(lines[i + 1].strip())
        ):

            merged.append(
                current + " " + lines[i + 1].strip()
            )

            i += 2
            continue

        # -------------------------
        # Case 2
        # Current line has letters
        # Next line starts with number
        # -------------------------

        if (
            i + 1 < len(lines)
            and re.search(r"[A-Za-z]", current)
            and re.match(r"^\d", lines[i + 1].strip())
        ):

            merged.append(
                current + " " + lines[i + 1].strip()
            )

            i += 2
            continue

        # -------------------------
        # Case 3
        # Three-line merge
        #
        # ITEM
        # Qty Price
        # Amount
        # -------------------------

        if (
            i + 2 < len(lines)
            and re.search(r"[A-Za-z]", current)
            and re.match(r"^\d", lines[i + 1].strip())
            and is_amount_only(lines[i + 2].strip())
        ):

            merged.append(
                current
                + " "
                + lines[i + 1].strip()
                + " "
                + lines[i + 2].strip()
            )

            i += 3
            continue

        merged.append(current)

        i += 1

    return merged