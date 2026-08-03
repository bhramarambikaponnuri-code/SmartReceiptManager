import re


def parse_item(line):
    """
    Parse a receipt item line.

    Returns:
        dict or None

    {
        "Qty": float,
        "Item": str,
        "Price": float,
        "Amount": float
    }
    """

    if not line:
        return None

    # ----------------------------
    # Cleaning
    # ----------------------------

    line = line.replace("₹", " ")
    line = line.replace(",", "")
    line = re.sub(r"\s+", " ", line).strip()

    # ----------------------------
    # Extract all numeric values
    # ----------------------------

    numbers = re.findall(r"\d+\.\d+|\d+", line)

    if len(numbers) < 3:
        return None

    try:

        qty = float(numbers[-3])

        price = float(numbers[-2])

        amount = float(numbers[-1])

    except ValueError:

        return None

    # ----------------------------
    # Extract item name
    # ----------------------------

    item_name = line

    # Remove numeric fields from the end only
    pattern = (
        rf"{re.escape(numbers[-3])}\s+"
        rf"{re.escape(numbers[-2])}\s+"
        rf"{re.escape(numbers[-1])}$"
    )

    item_name = re.sub(pattern, "", item_name).strip()

    # Remove trailing punctuation
    item_name = item_name.strip(":.- ")

    if len(item_name) < 2:
        return None

    return {

        "Qty": qty,

        "Item": item_name,

        "Price": price,

        "Amount": amount
    }