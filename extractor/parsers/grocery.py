from extractor.parsers.generic import GenericParser
from extractor.item_extractors.grocery_items import extract_grocery_items


class GroceryParser(GenericParser):
    """
    Parser for grocery receipts.

    Currently uses GenericParser.
    Later we'll add grocery-specific item extraction.
    """

    def __init__(self, text):
        super().__init__(text)

    def parse(self):

        data = super().parse()

        # Grocery-specific logic can be added here

        data["Items"] = extract_grocery_items(self.lines)

        return data