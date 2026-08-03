from extractor.item_extractors.detector import detect_item_lines
from extractor.item_extractors.cleaner import clean_item_line
from extractor.item_extractors.item_parser import parse_item
from extractor.item_extractors.validator import is_valid_item
from extractor.item_extractors.line_merger import merge_item_lines


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

        # Parse the item
        item = parse_item(line)

        if is_valid_item(item):
            items.append(item)

    print("\n========== FINAL ITEMS ==========")

    for item in items:
        print(item)

    return items