import re


IGNORE_WORDS = {
    "GST", "CGST", "SGST", "IGST",
    "TOTAL", "GRAND", "NET", "AMOUNT",
    "PAYABLE", "ROUND", "PAYMENT",
    "THANK", "VISIT", "WELCOME",
    "PHONE", "MOBILE", "ADDRESS",
    "EMAIL", "WEBSITE",
    "CASH", "CARD", "UPI",
    "BALANCE", "CHANGE", "TENDER",
    "SUBTOTAL", "DISCOUNT", "TAX",
    "DATE", "TIME",
    "BILL", "INVOICE",
    "OPERATOR",
    "CUSTOMER"
}


def _calculate_score(line: str) -> int:
    score = 0
    upper = line.upper()

    # Reject obvious headers/footers
    if any(word in upper for word in IGNORE_WORDS):
        return -100

    # Has alphabets
    if re.search(r"[A-Za-z]", line):
        score += 3

    # Has decimal amount
    if re.search(r"\d+\.\d{1,2}", line):
        score += 3

    # Has integer amount
    elif re.search(r"\b\d+\b", line):
        score += 1

    # Product-like words
    words = line.split()

    if 1 <= len(words) <= 8:
        score += 2

    # Penalize lines with too many numbers
    numbers = re.findall(r"\d+(?:\.\d+)?", line)

    if len(numbers) > 5:
        score -= 2

    # Reject lines that are only numbers
    if re.fullmatch(r"[\d .]+", line):
        score -= 4

    # Looks like quantity × price
    if re.search(r"[xX]\s*\d", line):
        score += 2

    # Weight based receipts
    if re.search(r"\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+", line):
        score += 2

    return score


def detect_item_lines(lines):
    """
    Detect probable receipt item lines using confidence scoring.
    """

    candidates = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        score = _calculate_score(line)

        if score >= 5:
            candidates.append(line)

    return candidates