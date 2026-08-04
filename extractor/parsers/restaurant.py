from extractor.parsers.generic import GenericParser

class RestaurantParser(GenericParser):
    """
    Parser for restaurant receipts.

    Currently uses GenericParser.
    Later we'll add restaurant-specific item extraction.
    """

    def __init__(self, text):
        super().__init__(text)

    def parse(self):

        return super().parse()