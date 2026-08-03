def create_tables(connection):

    cursor = connection.cursor()

    # Create receipts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts (

        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,

        receipt_type TEXT,

        store TEXT,

        customer TEXT,

        bill_no TEXT,

        date TEXT,

        gstin TEXT,

        total REAL,

        image_path TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create receipt items table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipt_items (

        item_id INTEGER PRIMARY KEY AUTOINCREMENT,

        receipt_id INTEGER,

        item_name TEXT,

        qty TEXT,

        price REAL,

        amount REAL,

        FOREIGN KEY(receipt_id)
        REFERENCES receipts(receipt_id)
    )
    """)

    connection.commit()