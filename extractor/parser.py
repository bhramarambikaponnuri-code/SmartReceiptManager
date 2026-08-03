from extractor.parsers.generic import GenericParser
from extractor.parsers.grocery import GroceryParser
from extractor.parsers.pharmacy import PharmacyParser
from extractor.parsers.restaurant import RestaurantParser


class ReceiptParser:

    def __init__(self, text, receipt_type="generic"):

        self.text = text
        self.receipt_type = receipt_type.lower()

    def parse(self):

        if self.receipt_type == "pharmacy":
            parser = PharmacyParser(self.text)

        elif self.receipt_type == "grocery":
            parser = GroceryParser(self.text)

        elif self.receipt_type == "restaurant":
            parser = RestaurantParser(self.text)

        else:
            parser = GenericParser(self.text)

        data = parser.parse()

        data["Receipt Type"] = self.receipt_type.title()

        return data