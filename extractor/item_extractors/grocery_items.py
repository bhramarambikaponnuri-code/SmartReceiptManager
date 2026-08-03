import re


IGNORE_WORDS = {
    "ITEM",
    "NAME",
    "WT",
    "QTY",
    "PRICE",
    "AMT",
    "TOTAL",
    "ROUND",
    "OFF",
    "THANK",
    "MC",
    "NO",
    "ITEMS",
}


def normalize_decimal(text):
    """
    Fix common OCR mistakes.
    """

    text = text.upper()

    text = text.replace("Q", "0")
    text = text.replace("O", "0")

    text = text.replace(":", ".")
    text = text.replace(";", ".")
    text = text.replace(",", ".")

    text = text.replace(" ", "")
    text = text.replace("'", "")
    text = text.replace('"', "")

    while ".." in text:
        text = text.replace("..", ".")

    # 0435 -> 0.435
    if re.fullmatch(r"\d{4}", text):
        text = text[0] + "." + text[1:]

    # 605 -> 0.605
    elif re.fullmatch(r"\d{3}", text):
        text = "0." + text

    # 41.3 -> 41.30
    elif re.fullmatch(r"\d+\.\d", text):
        text += "0"

    return text


def is_decimal(text):

    text = normalize_decimal(text)

    return re.fullmatch(r"\d+\.\d+", text) is not None


def is_item_name(text):
    """
    Check whether a line is likely to be a grocery item.
    """

    upper = text.upper()

    if any(word in upper for word in IGNORE_WORDS):
        return False

    if len(text.strip()) < 3:
        return False

    return any(ch.isalpha() for ch in text)


def extract_grocery_items(lines):
    """
    State-machine parser for grocery receipts.
    """

    items = []

    started = False
    i = 0

    while i < len(lines):

        line = lines[i].strip()
        upper = line.upper()

        # -------------------------
        # Find table start
        # -------------------------
        if not started:

            if "ITEM" in upper and "NAME" in upper:
                started = True
                i += 1

            else:
                i += 1

            continue

        # -------------------------
        # Stop parsing
        # -------------------------
        if any(word in upper for word in [
            "TOTAL",
            "THANK",
            "ROUND",
            "PAYMENT",
            "CASH"
        ]):
            break

        # -------------------------
        # Look for item name
        # -------------------------
        if is_item_name(line):

            item_name = line

            qty = ""
            price = ""
            amount = ""

            j = i + 1

            while j < len(lines):

                value = normalize_decimal(lines[j].strip())

                if is_decimal(value):

                    if qty == "":
                        qty = value

                    elif price == "":
                        price = value

                    elif amount == "":
                        amount = value
                        break

                # next item reached
                if is_item_name(lines[j]):
                    break

                j += 1

            print()
            print("Item :", item_name)
            print("Qty :", qty)
            print("Price :", price)
            print("Amount :", amount)

            if item_name and price and amount:

                items.append({

                    "Qty": qty,

                    "Item": item_name,

                    "Price": price,

                    "Amount": amount

                })

            i = j
            continue

        i += 1

    return items