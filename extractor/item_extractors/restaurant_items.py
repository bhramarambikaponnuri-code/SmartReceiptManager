import re


def extract_restaurant_items(lines):
    """
    Extract food items from restaurant receipts.

    Returns:
        List of dictionaries.
    """

    items = []

    start = False

    for line in lines:

        upper = line.upper()

        # Start after header
        if "ITEM" in upper and "PRICE" in upper:
            start = True
            continue

        if not start:
            continue

        # Stop at totals
        if any(word in upper for word in [
            "TOTAL",
            "VAT",
            "GST",
            "SERVICE",
            "NET",
            "AMOUNT"
        ]):
            break

        values = re.findall(r"\d+\.\d{2}", line)

        if len(values) >= 2:

            amount = values[-1]

            item = re.sub(r"\d+\.\d{2}", "", line)
            item = re.sub(r"\d+", "", item)
            item = item.strip()

            items.append({

                "Item": item,

                "Amount": amount

            })

    return items