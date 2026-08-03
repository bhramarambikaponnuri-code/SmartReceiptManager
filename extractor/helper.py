import re


def clean_text(text):
    """Remove extra spaces and tabs."""
    text = text.replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_lines(lines):
    """Remove empty lines."""
    return [clean_text(line) for line in lines if line.strip()]


def normalize_text(text):
    """
    Normalize common OCR mistakes.
    """

    replacements = {
        "Datenime": "Date Time",
        "Retum": "Return",
        "Savcd": "Saved",
        "Gencraled": "Generated",
        ",": ".",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def find_keyword(lines, keywords):
    """
    Find the first line containing any keyword.
    """

    for index, line in enumerate(lines):

        upper = line.upper()

        for keyword in keywords:

            if keyword.upper() in upper:
                return index

    return -1


def get_nearby_lines(lines, index, before=0, after=3):
    """
    Return nearby lines around a keyword.
    """

    start = max(0, index - before)
    end = min(len(lines), index + after + 1)

    return lines[start:end]


def extract_amount(text):
    """
    Extract decimal amount from OCR text.
    """

    # Convert comma decimal separator to dot
    text = text.replace(",", ".")

    # Remove currency prefixes
    text = text.replace("Rs.", "")
    text = text.replace("Rs-", "")
    text = text.replace("Rs", "")

    match = re.search(r"\d+\.\d{2}", text)

    if match:
        return match.group()

    return ""


def extract_integer(text):

    match = re.search(r"\d+", text)

    if match:
        return match.group()

    return ""