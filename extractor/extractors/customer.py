import re


CUSTOMER_KEYWORDS = [

    "CUSTOMER",
    "CUSTOMER NAME",

    "NAME",
    "PATIENT",
    "PATIENT NAME",

    "MEMBER",
    "MEMBER NAME",

    "BUYER",

    "SOLD TO",

    "CLIENT"
]


IGNORE_WORDS = [

    "DATE",
    "GST",
    "GSTIN",
    "PHONE",
    "MOBILE",
    "EMAIL",
    "ADDRESS",
    "DOCTOR",
    "BILL",
    "INVOICE",
    "TOTAL",
    "CASH",
    "CARD"
]


def is_valid_name(text):
    """
    Decide whether OCR text looks like a person's name.
    """

    text = text.strip()

    if len(text) < 3:
        return False

    upper = text.upper()

    # Ignore common receipt words
    if any(word in upper for word in IGNORE_WORDS):
        return False

    # Too many digits
    digits = sum(c.isdigit() for c in text)

    if digits > 2:
        return False

    # Must contain letters
    if not any(c.isalpha() for c in text):
        return False

    return True


def clean_name(text):

    text = re.sub(
        r"^(CUSTOMER|PATIENT|NAME|MEMBER)\s*[:\-]?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def find_customer(lines):
    """
    Smart customer name extractor.
    """

    for i, line in enumerate(lines):

        upper = line.upper()

        if any(keyword in upper for keyword in CUSTOMER_KEYWORDS):

            # ------------------------------------
            # Case 1
            # Customer : John Doe
            # ------------------------------------

            match = re.search(
                r":\s*(.+)$",
                line
            )

            if match:

                candidate = clean_name(match.group(1))

                if is_valid_name(candidate):
                    return candidate

            # ------------------------------------
            # Case 2
            # Customer
            # John Doe
            # ------------------------------------

            for j in range(i + 1, min(i + 4, len(lines))):

                candidate = clean_name(lines[j])

                if is_valid_name(candidate):
                    return candidate

    return ""