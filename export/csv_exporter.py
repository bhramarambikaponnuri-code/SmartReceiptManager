import pandas as pd


def export_receipt_csv(receipt_info, output_path):
    """
    Export receipt details to CSV.
    """

    receipt_data = receipt_info.copy()

    items = receipt_data.pop("Items", [])

    receipt_df = pd.DataFrame(
        receipt_data.items(),
        columns=["Field", "Value"]
    )

    items_df = pd.DataFrame(items)

    with open(output_path, "w", encoding="utf-8") as f:

        receipt_df.to_csv(
            f,
            index=False
        )

        f.write("\n\n")

        if not items_df.empty:

            items_df.to_csv(
                f,
                index=False
            )