import re


def clean_bill(text):
    """
    Clean OCR noise from bill number.
    """

    text = text.strip()

    # Remove common separators
    text = text.replace(":", "")
    text = text.replace("#", "")

    return text.strip()


def find_bill(lines):
    """
    Smart Bill / Invoice number extractor.
    """

    keywords = [

        "BILL",
        "BILL NO",
        "BILL NUMBER",

        "INVOICE",
        "INVOICE NO",
        "INVOICE NUMBER",

        "RECEIPT",
        "RECEIPT NO",

        "ORDER",
        "ORDER NO",

        "REF",
        "REF NO",

        "TXN",
        "TRANSACTION",
        "TRANSACTION ID",

        "DOC NO",
        "DOCUMENT NO"
    ]

    candidates = []

    for i, line in enumerate(lines):

        upper = line.upper()

        if any(keyword in upper for keyword in keywords):

            # Search current line + next 2 lines
            for j in range(i, min(i + 3, len(lines))):

                current = lines[j]

                # Alphanumeric bill numbers
                matches = re.findall(
                    r"[A-Z0-9][A-Z0-9/-]{4,25}",
                    current.upper()
                )

                for match in matches:

                    bill = clean_bill(match)

                    # Skip obvious keywords
                    if bill in {
                        "INVOICE",
                        "BILL",
                        "RECEIPT",
                        "ORDER",
                        "TOTAL",
                        "DATE"
                    }:
                        continue

                    candidates.append(bill)

    if candidates:

        # Prefer longer values (usually more complete)
        candidates.sort(
            key=len,
            reverse=True
        )

        return candidates[0]

    return ""