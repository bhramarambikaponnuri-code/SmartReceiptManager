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
    Extract grocery items.

    Expected format:

    ITEM_NAME   QTY   PRICE   AMOUNT
    """


    merged = []

    i = 0

    while i < len(lines):

        current = lines[i].strip()

        # item name only
        if (
            re.search(r"[A-Za-z]", current)
            and not re.search(r"\d+\.\d+", current)
            and i + 1 < len(lines)
        ):
            nxt = lines[i + 1].strip()

            if re.search(r"\d", nxt):

                merged.append(current + " " + nxt)

                i += 2

                continue

        merged.append(current)

        i += 1

    lines = merged

    items = []

    started = False

    for line in lines:

        upper = line.upper()

        # -------------------------
        # Wait until table starts
        # -------------------------
        if not started:

            if "ITEM" in upper and "NAME" in upper:
                started = True

            continue

        # -------------------------
        # Stop parsing
        # -------------------------
        if any(word in upper for word in [
            "MARKET",
            "OPERATOR",
            "ITEM NAME",
            "WT/QTY",
            "PRICE",
            "AMT",
            "TOTAL",
            "ROUND",
            "THANK",
            "PAYMENT",
            "CASH",
            "NO OF ITEMS",
            "T WT"
        ]):
            break

        # -------------------------
        # OCR cleanup
        # -------------------------
        line = line.upper()

        line = line.replace("_", " ")

        # Common OCR fixes
        line = line.replace('"', '.')
        line = line.replace("'", ".")
        line = line.replace("€", "0")
        line = line.replace("OQ", "00")
        line = line.replace("QQ", "00")
        line = line.replace("Q", "0")

        # Fix spaces around decimal points
        line = re.sub(r'(\d)\s*\.\s*(\d)', r'\1.\2', line)

        # Fix numbers like 64"0Q -> 64.00
        line = re.sub(r'(\d{2})["\']0Q', r'\1.00', line)

        # Fix 3'€Q -> 3.00
        line = re.sub(r'(\d)["\']?€?Q', r'\1.00', line)

        # convert comma decimals
        line = re.sub(r"(\d),(\d{2,3})", r"\1.\2", line)

        line = re.sub(r"\s+", " ", line).strip()

        line = re.sub(r'(\d+)\.\s+(\d{2})', r'\1.\2', line)

        # Collapse multiple spaces
        line = re.sub(r'\s+', ' ', line).strip()

        line = re.sub(r'^\d+\s+', '', line)


        # Convert weights like 435 -> 0.435
        line = re.sub(
            r'(?<=\s)(\d{3})(?=\s+\d+\.\d+\s+\d+\.\d+)',
            r'0.\1',
            line
        )

        # Convert weights like 805 -> 0.805
        line = re.sub(
            r'(?<=\s)(\d{4})(?=\s+\d+\.\d+\s+\d+\.\d+)',
            lambda m: "0." + m.group(1),
            line
        )

        # Fix 37 .80 -> 37.80
        line = re.sub(
            r'(\d+)\s+\.\s*(\d{2})',
            r'\1.\2',
            line
        )

        # -------------------------
        # Extract decimal numbers
        # -------------------------
        numbers = re.findall(r"\d+\.\d+", line)

        print()
        print("LINE :", line)
        print("NUMBERS :", numbers)

        qty = None
        price = None
        amount = None

        # -------------------------
        # Parse numbers
        # -------------------------
        if len(numbers) >= 3:

            qty = float(numbers[-3])
            price = float(numbers[-2])
            amount = float(numbers[-1])

        elif len(numbers) == 2:

            # Quantity missing -> assume 1
            qty = 1
            price = float(numbers[-2])
            amount = float(numbers[-1])

        else:
            continue

        # OCR sometimes gives wrong amount
        if amount < price:
            amount = round(qty * price, 2)

        # Everything before Qty is item name
        item = line.split(numbers[0])[0].strip()

        item = item.replace('"', "").replace("'", "")

        if len(item) < 2:
            continue

        items.append({

            "Qty": qty,
            "Item": item.title(),
            "Price": round(price, 2),
            "Amount": round(amount, 2)

        })

    return items