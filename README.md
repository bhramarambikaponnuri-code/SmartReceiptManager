# 🧾 Smart Receipt Manager

An AI-powered Receipt Information Extraction and Expense Management System built using **Python**, **Streamlit**, **EasyOCR**, and **SQLite**.

The application automatically extracts important information from scanned receipts, stores the data in a database, allows editing of extracted information, maintains receipt history, provides expense analytics, and exports receipts in multiple formats.

---

# 📌 Features

## OCR & Image Processing

- Upload receipt images (JPG, JPEG, PNG)
- Automatic receipt scanning
- Image preprocessing
- Automatic rotation correction
- OCR using EasyOCR

---

## Intelligent Receipt Parsing

The system automatically extracts:

- Store Name
- Store Number
- Receipt Number
- Receipt Date
- Customer Name
- GSTIN
- Total Amount
- Individual Purchased Items
- Quantity
- Price
- Amount

Supports:

- Grocery Receipts
- Pharmacy Receipts
- Restaurant Bills
- Generic Receipts

---

## Receipt Management

- Save receipts into SQLite database
- View receipt history
- Search receipts
- Edit receipt details
- Update receipt information
- Delete receipts

---

## Dashboard

Visual analytics including:

- Total Expenses
- Category-wise Expenses
- Monthly Expense Trend
- Number of Receipts
- Spending Distribution

---

## Export Options

Export receipt details as:

- CSV
- Excel (.xlsx)
- PDF

---

## Settings

- View application information
- Storage statistics
- Clear receipt history
- Delete uploaded images
- Delete exported files
- Reset application

---

# 🏗 Project Architecture

```
Receipt Image
        │
        ▼
Document Scanner
        │
        ▼
Image Preprocessing
        │
        ▼
EasyOCR
        │
        ▼
Text Extraction
        │
        ▼
Receipt Parser
        │
        ▼
SQLite Database
        │
        ▼
Dashboard • History • Export
```

---

# 🗂 Project Structure

```
ReceiptExtractor/

│
├── app.py
├── requirements.txt
├── README.md
├── receipt.db
│
├── database/
│
├── extractor/
│   ├── extractors/
│   ├── item_extractors/
│   └── parsers/
│
├── export/
│
├── ocr/
│
├── ui/
│
├── uploads/
│
├── exports/
│
└── .streamlit/
```

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend |
| Streamlit | User Interface |
| EasyOCR | OCR Engine |
| OpenCV | Image Processing |
| SQLite | Database |
| Pandas | Data Processing |
| OpenPyXL | Excel Export |
| ReportLab | PDF Export |

---

# 🚀 Installation

## Clone Project

```bash
git clone <repository_url>
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📷 Screenshots

(Add screenshots here)

- Home Page
- OCR Extraction
- History
- Dashboard
- Settings
- Export

---

# 🎯 Future Enhancements

- Multi-language OCR
- Cloud Database
- Barcode & QR Detection
- Receipt Classification using Deep Learning
- Mobile Application
- REST API Integration

---

# 👩‍💻 Author

**Bhramarambika Ponnuri**

AI & Machine Learning Diploma Project

University of Hyderabad

---

# 📄 License

This project is developed for academic purposes as part of the AI & Machine Learning Diploma.