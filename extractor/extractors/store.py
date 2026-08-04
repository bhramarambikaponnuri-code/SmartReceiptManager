import re


def is_address(line):
    """
    Returns True if the line looks like an address.
    """

    text = line.upper()

    keywords = [
        "ROAD",
        "RD",
        "STREET",
        "NAGAR",
        "COLONY",
        "LANE",
        "AREA",
        "CITY",
        "STATE",
        "PIN",
        "HYDERABAD",
        "TELANGANA",
        "INDIA",
        "PHONE",
        "MOBILE"
    ]

    return any(word in text for word in keywords)


def find_store(lines):
    """
    Find the most likely store name using a scoring system.
    """

    best_score = -1
    best_store = ""

    # Only the top portion of the receipt
    for idx, line in enumerate(lines[:12]):

        text = line.strip()

        if len(text) < 3:
            continue

        upper = text.upper()

        score = 0

        # Higher preference for top lines
        if idx < 5:
            score += 3

        # --------------------------
        # Positive scoring
        # --------------------------

        # Mostly alphabets
        letters = sum(c.isalpha() for c in text)

        if letters >= 5:
            score += 3

        # Few digits
        digits = sum(c.isdigit() for c in text)

        if digits <= 2:
            score += 2

        # Uppercase looks like business name
        if upper == text:
            score += 2

        # Reward Title Case
        if text.istitle():
            score += 2

        # Not too long
        if len(text) <= 35:
            score += 1

        # --------------------------
        # Bonus for known business words
        # --------------------------

        business_words = [
            "MART",
            "STORE",
            "SUPERMARKET",
            "SUPER",
            "MEDICAL",
            "PHARMACY",
            "HOSPITAL",
            "CLINIC",
            "RESTAURANT",
            "HOTEL",
            "CAFE",
            "BAKERY",
            "FOODS",
            "MARKET",
            "ENTERPRISES",
            "ENTERPRISE",
            "TRADERS",
            "TRADING",
            "JEWELLERS",
            "JEWELERS",
            "OPTICAL",
            "OPTICS",
            "ELECTRONICS",
            "MOBILE",
            "FASHION",
            "TEXTILES",
            "PVT",
            "PRIVATE",
            "LIMITED",
            "LTD",
            "LLP"
        ]

        if any(word in upper for word in business_words):
            score += 4

        # --------------------------
        # Negative scoring
        # --------------------------

        bad_words = [
            "GST",
            "GSTIN",
            "PHONE",
            "TEL",
            "MOBILE",
            "EMAIL",
            "WEBSITE",
            "INVOICE",
            "BILL",
            "RECEIPT",
            "DATE",
            "TIME",
            "TAX",
            "TOTAL",
            "AMOUNT",
            "CASH",
            "CARD",
            "UPI",
            "WELCOME",
            "THANK",
            "VISIT",
            "CUSTOMER",
            "CASHIER",
            "CHANGE",
            "BALANCE",
            "ROUND",
            "DISCOUNT"
        ]

        if any(word in upper for word in bad_words):
            score -= 6

        if is_address(text):
            score -= 3

        if digits > 5:
            score -= 3

        # --------------------------

        if score > best_score:
            best_score = score
            best_store = text

    # Don't return weak candidates
    if best_score < 3:
        return ""

    return best_store