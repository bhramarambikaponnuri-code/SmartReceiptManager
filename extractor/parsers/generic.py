from extractor.fields import (
    find_store,
    find_customer,
    find_bill,
    find_date,
    find_gstin,
    find_total,
    find_items
)


class GenericParser:

    def __init__(self, text):

        self.text = text

        self.lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

    def parse(self):

        return {

            "Store": find_store(self.lines),

            "Customer": find_customer(self.lines),

            "Bill No": find_bill(self.lines),

            "Date": find_date(self.lines),

            "GSTIN": find_gstin(self.lines),

            "Total": find_total(self.lines),

            "Items": find_items(self.lines)
        }