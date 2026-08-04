import re
from datetime import datetime


def normalize_date(date_str):
    """
    Convert different date formats into DD/MM/YYYY.
    """

    formats = [

        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d.%m.%Y",

        "%Y-%m-%d",

        "%d/%m/%y",
        "%d-%m-%y",
        "%d.%m.%y",

        "%d %b %Y",
        "%d %B %Y",

        "%d %b %y",
        "%d %B %y",

        "%b %d %Y",
        "%B %d %Y",

        "%b %d %y",
        "%B %d %y",

        "%d%b%Y",
        "%d%b%y",

        "%d-%b-%Y",
        "%d-%b-%y",

        "%d-%B-%Y",
        "%d-%B-%y",
    ]

    for fmt in formats:

        try:

            dt = datetime.strptime(date_str.strip(), fmt)

            return dt.strftime("%d/%m/%Y")

        except Exception:
            pass

    return None


def clean_ocr_date(text):
    """
    Correct common OCR mistakes.
    """

    text = text.replace("O", "0")
    text = text.replace("o", "0")

    text = text.replace("I", "1")
    text = text.replace("l", "1")

    text = text.replace("\\", "/")
    text = text.replace("|", "/")

    return text


def find_date(lines):
    """
    Smart date extractor using confidence scoring.
    """

    candidates = []

    keyword_scores = {

        "BILL DATE": 120,
        "INVOICE DATE": 120,
        "TRANSACTION DATE": 115,
        "PURCHASE DATE": 110,
        "DATE": 100,

        "EXPIRY": -100,
        "EXP": -100,
        "MFG": -100,
        "MANUFACTURED": -100,
        "PACKED": -80,
        "BEST BEFORE": -100,
        "TIME": -20
    }

    patterns = [

        # 14/07/2025
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",

        # 14.07.2025
        r"\d{1,2}\.\d{1,2}\.\d{2,4}",

        # 2025-07-14
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}",

        # 14 Jul 2025
        r"\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4}",

        # Jul 14 2025
        r"[A-Za-z]{3,9}\s+\d{1,2}\s+\d{2,4}",

        # 03AUG2026
        r"\d{2}[A-Za-z]{3}\d{4}",

        # 03-Aug-26
        r"\d{2}-[A-Za-z]{3}-\d{2,4}",
    ]

    for idx, line in enumerate(lines):

        line = clean_ocr_date(line)

        line = line.replace("Datenime", "Date")
        line = line.replace("Datetime", "Date")

        upper = line.upper()

        score = 0

        for key, value in keyword_scores.items():

            if key in upper:
                score += value

        # Small bonus for dates near top of receipt
        score += max(0, 20 - idx)

        for pattern in patterns:

            matches = re.findall(pattern, line)

            for match in matches:

                normalized = normalize_date(match)

                if normalized:

                    candidates.append((score, normalized))

        # Handle OCR like 14/072025
        match = re.search(r"(\d{2})/(\d{2})(\d{4})", line)

        if match:

            reconstructed = (
                f"{match.group(1)}/"
                f"{match.group(2)}/"
                f"{match.group(3)}"
            )

            normalized = normalize_date(reconstructed)

            if normalized:

                candidates.append((score, normalized))

    if not candidates:
        return ""

    # Keep highest score for duplicate dates
    best_dates = {}

    for score, date in candidates:

        if date not in best_dates:

            best_dates[date] = score

        else:

            best_dates[date] = max(best_dates[date], score)

    # Highest confidence wins
    best_date = max(
        best_dates.items(),
        key=lambda x: x[1]
    )[0]

    return best_date