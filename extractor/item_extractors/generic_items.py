from extractor.item_extractors.detector import detect_item_lines
from extractor.item_extractors.cleaner import clean_item_line
from extractor.item_extractors.item_parser import parse_item, looks_like_item
from extractor.item_extractors.validator import is_valid_item
from extractor.item_extractors.line_merger import merge_item_lines
from extractor.extractors.store import is_address


def extract_generic_items(lines):
    """
    Generic item extractor.

    Pipeline:
        OCR Lines
            ↓
        Detector
            ↓
        Cleaner
            ↓
        Item Parser
            ↓
        Return Parsed Items
    """

    items = []

    # Merge OCR split lines first
    lines = merge_item_lines(lines)

    print("\n===== MERGED LINES =====")

    for line in lines:
        print(line)

    print("========================\n")

    print("\n========== AFTER MERGING ==========")

    for line in lines:
        print(line)

    # Detect candidate item rows
    candidate_lines = detect_item_lines(lines)

    print("\n========== DETECTED LINES ==========")

    for line in candidate_lines:
        print(line)

    for line in candidate_lines:

        # Clean OCR noise
        line = clean_item_line(line)

        skip_words = [
            "TOTAL",
            "SUB TOTAL",
            "SUBTOTAL",
            "GRAND TOTAL",
            "GST",
            "CGST",
            "SGST",
            "IGST",
            "TAX",
            "CASHIER",
            "TOKEN",
            "NAME",
            "DATE",
            "TIME",
            "FSSAI",
            "PHONE",
            "MOBILE",
            "THANK",
            "VISIT",
            "ADDRESS",
            "QTY",
            "AMOUNT",
            "PRICE"
        ]

        upper = line.upper()

        if any(word in upper for word in skip_words):
            continue

        if is_address(line):
            continue

        upper = line.upper()

        if (
            "GST" in upper
            or "DATE" in upper
            or "TOKEN" in upper
            or "FSSAI" in upper
            or "NAME" == upper.strip(": ")
        ):
            continue

        # Parse the item
        if not looks_like_item(line):
            continue

        print("Parsing:", line)

        item = parse_item(line)
        print(item)

        if is_valid_item(item):
            items.append(item)

    print("\n========== FINAL ITEMS ==========")

    for item in items:
        print(item)

    return items