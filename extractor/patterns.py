import re

# -------------------------
# Common Patterns
# -------------------------

DATE_PATTERN = re.compile(
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
)

TIME_PATTERN = re.compile(
    r"\b\d{1,2}:\d{2}\b"
)

# Official GSTIN format
GSTIN_PATTERN = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)

BILL_PATTERN = re.compile(
    r"Bill\s*No\.?\s*:?\s*([A-Za-z0-9\-]+)",
    re.IGNORECASE
)

INVOICE_PATTERN = re.compile(
    r"Invoice\s*No\.?\s*:?\s*([A-Za-z0-9\-]+)",
    re.IGNORECASE
)

TOTAL_PATTERN = re.compile(
    r"(Net Amount|Total)\s*[:\-]?\s*Rs\.?\s*([0-9]+\.[0-9]{2})",
    re.IGNORECASE
)