from extractor.parsers.generic import GenericParser
from extractor.item_extractors.restaurant_items import extract_restaurant_items


class RestaurantParser(GenericParser):
    """
    Parser for restaurant receipts.

    Currently uses GenericParser.
    Later we'll add restaurant-specific item extraction.
    """

    def __init__(self, text):
        super().__init__(text)

    def parse(self):

        data = super().parse()

        data["Items"] = extract_restaurant_items(self.lines)

        return data