from extractor.parsers.generic import GenericParser
from extractor.item_extractors.pharmacy_items import extract_pharmacy_items


class PharmacyParser(GenericParser):
    """
    Parser for pharmacy receipts.
    """

    def __init__(self, text):
        super().__init__(text)

    def parse(self):

        data = super().parse()

        # Replace generic item extraction
        data["Items"] = extract_pharmacy_items(self.lines)

        return data