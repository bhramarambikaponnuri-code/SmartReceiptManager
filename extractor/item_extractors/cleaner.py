import re


def clean_item_line(line):
    """
    Clean OCR text before parsing.

    This function only normalizes text.
    It does NOT extract qty/price/items.
    """

    if not line:
        return ""

    # ----------------------------------
    # Remove leading/trailing spaces
    # ----------------------------------

    line = line.strip()

    # ----------------------------------
    # Replace tabs with spaces
    # ----------------------------------

    line = line.replace("\t", " ")

    # ----------------------------------
    # Remove common OCR separators
    # ----------------------------------

    line = line.replace("|", " ")
    line = line.replace("¦", " ")
    line = line.replace(":", " ")

    # ----------------------------------
    # Remove currency symbols
    # ----------------------------------

    line = line.replace("₹", "")
    line = line.replace("Rs.", "")
    line = line.replace("Rs", "")
    line = line.replace("INR", "")

    # ----------------------------------
    # Fix common OCR mistakes
    # ----------------------------------

    replacements = {

        "O.00": "0.00",
        "O.OO": "0.00",
        "OO.00": "00.00",

        " x ": " ",
        " X ": " ",

    }

    for old, new in replacements.items():
        line = line.replace(old, new)

    # ----------------------------------
    # Remove thousands separators
    # Example:
    # 1,250.00 -> 1250.00
    # ----------------------------------

    line = re.sub(r"(?<=\d),(?=\d{3}\b)", "", line)

    # ----------------------------------
    # Collapse multiple spaces
    # ----------------------------------

    line = re.sub(r"\s+", " ", line)

    # ----------------------------------
    # Remove trailing punctuation
    # ----------------------------------

    line = re.sub(r"[;,_-]+$", "", line)

    return line.strip()