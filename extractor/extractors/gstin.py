import re

from extractor.patterns import GSTIN_PATTERN


def normalize_gstin(candidate):
    """
    Fix common OCR mistakes.
    """

    candidate = candidate.upper()

    # GSTIN is always 15 characters
    if len(candidate) != 15:
        return candidate

    chars = list(candidate)

    # State code (0-1) must be digits
    for i in [0, 1]:
        if chars[i] == "O":
            chars[i] = "0"

    # PAN digits (7-10)
    for i in [7, 8, 9, 10]:
        if chars[i] == "O":
            chars[i] = "0"

        if chars[i] == "I":
            chars[i] = "1"

    # Entity code (12)
    if chars[12] == "O":
        chars[12] = "0"

    # Z position (13)
    if chars[13] == "2":
        chars[13] = "Z"

    return "".join(chars)


def find_gstin(lines):
    """
    Extract GSTIN using official validation.
    """

    for line in lines:

        text = line.upper().replace(" ", "")

        candidates = re.findall(r"[A-Z0-9]{15}", text)

        for candidate in candidates:

            candidate = normalize_gstin(candidate)

            if GSTIN_PATTERN.match(candidate):
                return candidate

    return ""