import re
from extractor.helper import extract_amount


def find_total(lines):

    candidates = []

    positive_scores = {
        "AMOUNT PAYABLE": 100,
        "NET AMOUNT": 95,
        "GRAND TOTAL": 90,
        "TOTAL": 80,
    }

    negative_keywords = {
        "SUB TOTAL",
        "ITEM TOTAL",
        "DISCOUNT",
        "CGST",
        "SGST",
        "IGST",
        "TAX",
        "ROUND",
        "CHANGE",
        "CASH",
        "RECEIVED",
        "BALANCE",
        "MRP",
        "SAVINGS",
    }

    for i, line in enumerate(lines):

        upper = line.upper()

        # Skip obvious non-total lines
        if any(word in upper for word in negative_keywords):
            continue

        amount = None

        # Check current line and next 2 lines
        for j in range(i, min(i + 3, len(lines))):

            amount = extract_amount(lines[j])

            if amount:
                break

        if not amount:
            continue

        score = 0

        for keyword, value in positive_scores.items():
            if keyword in upper:
                score = value
                break

        # Bonus for appearing near bottom of receipt
        score += max(0, i - len(lines) + 20)

        candidates.append(
            (
                score,
                float(amount),
                amount
            )
        )

    # If confidence candidates exist
    if candidates:

        candidates.sort(
            key=lambda x: (
                x[0],      # confidence
                x[1]       # larger amount
            ),
            reverse=True
        )

        return candidates[0][2]

    # ----------------------
    # Final fallback
    # ----------------------

    amounts = []

    for line in lines[-15:]:

        values = re.findall(r"\d+\.\d{2}", line)

        for value in values:

            try:
                amounts.append(float(value))
            except:
                pass

    if amounts:
        return f"{max(amounts):.2f}"

    return ""