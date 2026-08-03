import re


def extract_items(lines):
    """
    Extract purchased items from OCR text.
    """

    items = []

    for line in lines:

        line = line.strip()

        # Skip very short lines
        if len(line) < 8:
            continue

        # Ignore obvious header/footer lines
        ignore = [
            "TOTAL",
            "NET",
            "GST",
            "CGST",
            "SGST",
            "PHONE",
            "DATE",
            "TIME",
            "BILL",
            "INVOICE",
            "THANK",
            "CASH",
            "MODE",
        ]

        if any(word in line.upper() for word in ignore):
            continue

        # Find decimal numbers
        numbers = re.findall(r"\d+\.\d{2}", line)

        if len(numbers) < 2:
            continue

        amount = numbers[-1]
        price = numbers[-2]

        # Everything before first decimal is item name
        index = line.find(price)

        item_name = line[:index].strip()

        qty_match = re.search(r"\d+", item_name)

        qty = ""

        if qty_match:
            qty = qty_match.group()
            item_name = item_name.replace(qty, "").strip()

        items.append({
            "item": item_name,
            "qty": qty,
            "price": price,
            "amount": amount
        })

    return items