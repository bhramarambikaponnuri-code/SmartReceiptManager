from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


def export_receipt_pdf(receipt_info, output_path):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(output_path)

    elements = []

    # ---------------------------------------
    # Title
    # ---------------------------------------

    elements.append(
        Paragraph(
            "<b>Smart Receipt Manager</b>",
            styles["Title"]
        )
    )

    elements.append(
        Paragraph(
            "AI Powered Receipt Information Extractor",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------
    # Receipt Details
    # ---------------------------------------

    data = [["Field", "Value"]]

    for key, value in receipt_info.items():

        if key == "Items":
            continue

        data.append([key, str(value)])

    table = Table(data, colWidths=[2.2 * inch, 3.3 * inch])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke)

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 0.3 * inch))

    # ---------------------------------------
    # Purchased Items
    # ---------------------------------------

    elements.append(

        Paragraph(

            "<b>Purchased Items</b>",

            styles["Heading2"]

        )

    )

    item_rows = [[

        "Qty",

        "Item",

        "Price",

        "Amount"

    ]]

    for item in receipt_info.get("Items", []):

        item_rows.append([

            str(item.get("Qty", "")),

            item.get("Item", ""),

            str(item.get("Price", "")),

            str(item.get("Amount", ""))

        ])

    item_table = Table(

        item_rows,

        colWidths=[0.8 * inch, 2.8 * inch, 1 * inch, 1 * inch]

    )

    item_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#06B6D4")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige)

        ])

    )

    elements.append(item_table)

    doc.build(elements)