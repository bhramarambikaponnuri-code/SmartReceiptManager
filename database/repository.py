from database.database import get_connection


class ReceiptRepository:

    def __init__(self):
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

    def save_receipt(self, data, image_path):
        """
        Save receipt header information.

        Returns:
            receipt_id
        """

        self.cursor.execute(
            """
            INSERT INTO receipts
            (
                receipt_type,
                store,
                customer,
                bill_no,
                date,
                gstin,
                total,
                image_path
            )

            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("Receipt Type", ""),
                data.get("Store", ""),
                data.get("Customer", ""),
                data.get("Bill No", ""),
                data.get("Date", ""),
                data.get("GSTIN", ""),
                data.get("Total", ""),
                image_path
            )
        )

        self.connection.commit()

        return self.cursor.lastrowid

    def save_items(self, receipt_id, items):
        """
        Save all receipt items.
        """

        for item in items:

            self.cursor.execute(
                """
                INSERT INTO receipt_items
                (
                    receipt_id,
                    item_name,
                    qty,
                    price,
                    amount
                )

                VALUES
                (?, ?, ?, ?, ?)
                """,
                (
                    receipt_id,
                    item.get("Item", ""),
                    item.get("Qty", ""),
                    item.get("Price", ""),
                    item.get("Amount", "")
                )
            )

        self.connection.commit()

    def get_receipts(self):
        """
        Returns all saved receipts.
        """

        self.cursor.execute("""
            SELECT
                receipt_id,
                receipt_type,
                store,
                customer,
                bill_no,
                date,
                total
            FROM receipts
            ORDER BY receipt_id DESC
        """)

        return self.cursor.fetchall()
    
    def get_receipt(self, receipt_id):
        """
        Returns a single receipt.
        """

        self.cursor.execute(
            """
            SELECT *
            FROM receipts
            WHERE receipt_id = ?
            """,
            (receipt_id,)
        )

        return self.cursor.fetchone()
    
    def get_items(self, receipt_id):
        """
        Returns all items belonging to a receipt.
        """

        self.cursor.execute(
            """
            SELECT
                item_name,
                qty,
                price,
                amount
            FROM receipt_items
            WHERE receipt_id = ?
            ORDER BY item_id
            """,
            (receipt_id,)
        )

        return self.cursor.fetchall()


    def search_receipts(self, keyword):
        """
        Search receipts by store, customer or bill number.
        """

        self.cursor.execute(
            """
            SELECT
                receipt_id,
                receipt_type,
                store,
                customer,
                bill_no,
                date,
                total
            FROM receipts
            WHERE
                store LIKE ?
                OR customer LIKE ?
                OR bill_no LIKE ?
            ORDER BY receipt_id DESC
            """,
            (
                f"%{keyword}%",
                f"%{keyword}%",
                f"%{keyword}%"
            )
        )

        return self.cursor.fetchall()
    
    def get_image_path(self, receipt_id):

        self.cursor.execute(
            """
            SELECT image_path
            FROM receipts
            WHERE receipt_id = ?
            """,
            (receipt_id,)
        )

        row = self.cursor.fetchone()

        if row:
            return row[0]

        return None
    
    def get_total_receipts(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM receipts
        """)

        return self.cursor.fetchone()[0]
    
    def get_total_amount(self):

        self.cursor.execute("""
            SELECT IFNULL(SUM(total), 0)
            FROM receipts
        """)

        return self.cursor.fetchone()[0]
    
    def get_total_stores(self):

        self.cursor.execute("""
            SELECT COUNT(DISTINCT store)
            FROM receipts
        """)

        return self.cursor.fetchone()[0]
    
    def get_total_items(self):

        self.cursor.execute("""
            SELECT COUNT(*)
            FROM receipt_items
        """)

        return self.cursor.fetchone()[0]

    def get_receipt_type_distribution(self):
        """
        Returns receipt count grouped by receipt type.
        """

        self.cursor.execute("""
            SELECT
                receipt_type,
                COUNT(*)
            FROM receipts
            GROUP BY receipt_type
            ORDER BY COUNT(*) DESC
        """)

        return self.cursor.fetchall()
    
    def get_top_stores(self, limit=5):
        """
        Returns the top stores by number of receipts.
        """

        self.cursor.execute(
            """
            SELECT
                store,
                COUNT(*) AS receipts,
                IFNULL(SUM(total), 0) AS total_spent
            FROM receipts
            WHERE store <> ''
            GROUP BY store
            ORDER BY receipts DESC, total_spent DESC
            LIMIT ?
            """,
            (limit,)
        )

        return self.cursor.fetchall()
    
    def get_top_items(self, limit=10):
        """
        Returns the most frequently purchased items.
        """

        self.cursor.execute(
            """
            SELECT
                item_name,
                COUNT(*) AS purchase_count
            FROM receipt_items
            WHERE item_name <> ''
            GROUP BY item_name
            ORDER BY purchase_count DESC, item_name
            LIMIT ?
            """,
            (limit,)
        )

        return self.cursor.fetchall()
    
    def get_monthly_spending(self):
        """
        Returns total spending grouped by month.
        """

        self.cursor.execute("""
            SELECT
                substr(date, 1, 7) AS month,
                IFNULL(SUM(total), 0) AS total_spent
            FROM receipts
            WHERE date IS NOT NULL
            AND date <> ''
            GROUP BY month
            ORDER BY month
        """)

        return self.cursor.fetchall()
    
    def update_receipt(self, receipt_id, info):

        self.cursor.execute(
            """
            UPDATE receipts
            SET
                receipt_type=?,
                store=?,
                customer=?,
                bill_no=?,
                date=?,
                gstin=?,
                total=?
            WHERE receipt_id=?
            """,
            (
                info["Receipt Type"],
                info["Store"],
                info["Customer"],
                info["Bill No"],
                info["Date"],
                info["GSTIN"],
                info["Total"],
                receipt_id
            )
        )

        self.connection.commit()

    def delete_items(self, receipt_id):

        self.cursor.execute(
            """
            DELETE FROM receipt_items
            WHERE receipt_id=?
            """,
            (receipt_id,)
        )

        self.connection.commit()

    def delete_receipt(self, receipt_id):

        image_path = self.get_image_path(receipt_id)

        self.cursor.execute(
            "DELETE FROM receipt_items WHERE receipt_id=?",
            (receipt_id,)
        )

        self.cursor.execute(
            "DELETE FROM receipts WHERE receipt_id=?",
            (receipt_id,)
        )

        self.connection.commit()

        if image_path:

            import os

            if os.path.exists(image_path):
                os.remove(image_path)

    def close(self):
        self.connection.close()