import re


def is_decimal(text):
    """
    Returns True if text looks like 12.34
    """
    return re.fullmatch(r"\d+\.\d{2}", text.strip()) is not None


def extract_pharmacy_items(lines):
    """
    Extract medicine details from pharmacy receipt.
    """

    items = []

    start = False
    i = 0

    while i < len(lines):

        line = lines[i].strip()
        upper = line.upper()

        # -----------------------
        # Find start of item table
        # -----------------------
        if "PRODUCT NAME" in upper:
            start = True
            i += 1
            continue

        if not start:
            i += 1
            continue

        # -----------------------
        # Stop at totals
        # -----------------------
        if any(word in upper for word in [
            "SGST",
            "CGST",
            "TOTAL",
            "NET AMOUNT"
        ]):
            break

        # -----------------------
        # Quantity
        # -----------------------
        if line.isdigit():

            qty = int(line)

            # Ignore Pack/HSN/Batch numbers
            if qty > 20:
                i += 1
                continue

            if i + 1 >= len(lines):
                break

            item_name = lines[i + 1].strip()

            # Item name must contain letters
            if not any(c.isalpha() for c in item_name):
                i += 1
                continue

            # Search next few lines for decimal values
            decimals = []

            for j in range(i + 2, min(i + 12, len(lines))):

                if is_decimal(lines[j]):
                    decimals.append(lines[j])

            print(f"\nDetected Qty      : {qty}")
            print(f"Detected Medicine : {item_name}")
            print("Decimals Found    :", decimals)

            price = ""
            amount = ""

            if len(decimals) >= 3:
                price = decimals[1]
                amount = decimals[2]

            items.append({

                "Qty": str(qty),

                "Item": item_name,

                "Price": price,

                "Amount": amount

            })

        i += 1

    return items