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

        "%d %b %Y",
        "%d %B %Y",

        "%d %b %y",
        "%d %B %y",

        "%b %d %Y",
        "%B %d %Y",

        "%b %d %y",
        "%B %d %y",
    ]

    for fmt in formats:

        try:

            dt = datetime.strptime(date_str.strip(), fmt)

            return dt.strftime("%d/%m/%Y")

        except:
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
    Smart date extractor.

    Supports many receipt formats and OCR mistakes.
    """

    candidates = []

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
    ]

    for line in lines:

        line = clean_ocr_date(line)

        # Correct OCR keyword mistakes
        line = line.replace("Datenime", "Date")
        line = line.replace("Datetime", "Date")

        for pattern in patterns:

            matches = re.findall(pattern, line)

            for match in matches:

                normalized = normalize_date(match)

                if normalized:

                    candidates.append(normalized)

        # Handle OCR like 14/072025
        match = re.search(r"(\d{2})/(\d{2})(\d{4})", line)

        if match:

            reconstructed = f"{match.group(1)}/{match.group(2)}/{match.group(3)}"

            normalized = normalize_date(reconstructed)

            if normalized:

                candidates.append(normalized)

    if candidates:

        # Remove duplicates while preserving order
        unique = list(dict.fromkeys(candidates))

        return unique[0]

    return ""