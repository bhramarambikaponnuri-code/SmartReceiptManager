import re
from extractor.helper import extract_amount


def find_total(lines):
    """
    Extract the final payable amount.

    Priority:
        1. Amount Payable
        2. Net Amount
        3. Grand Total
        4. Total
        5. Largest amount near end of receipt
    """

    priority_keywords = [

        "AMOUNT PAYABLE",
        "NET AMOUNT",
        "GRAND TOTAL",
        "TOTAL"
    ]

    ignore_keywords = [

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
        "SAVINGS"
    ]

    # ------------------------
    # Priority search
    # ------------------------

    for keyword in priority_keywords:

        for i, line in enumerate(lines):

            upper = line.upper()

            if keyword not in upper:
                continue

            if any(ignore in upper for ignore in ignore_keywords):
                continue

            for j in range(i, min(i + 3, len(lines))):

                amount = extract_amount(lines[j])

                if amount:
                    return amount

    # ------------------------
    # Fallback:
    # Largest amount near bottom
    # ------------------------

    amounts = []

    for line in lines[-15:]:

        upper = line.upper()

        if any(ignore in upper for ignore in ignore_keywords):
            continue

        values = re.findall(r"\d+\.\d{2}", line)

        for value in values:

            try:
                amounts.append(float(value))
            except:
                pass

    if amounts:
        return f"{max(amounts):.2f}"

    return ""