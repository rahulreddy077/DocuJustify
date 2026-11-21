# DocuJustify

DocuJustify is a FastAPI-powered backend engine for document verification and financial justification analysis. It extracts text and key financial details from diverse document formats (Images, PDFs, CSVs, Plain Text) and computes repayment feasibility assessments.

---

## Features

- **Multi-Format Text Extraction**:
  - **Images (`.png`, `.jpg`, `.jpeg`)**: Powered by OCR via Tesseract (`pytesseract`) & PIL (`Pillow`).
  - **PDFs (`.pdf`)**: Extracted using `pdfplumber`.
  - **Spreadsheets (`.csv`)**: Parsed via `pandas`.
  - **Text files (`.txt`)**: Plain text parsing.
- **Field Extraction**: Automatically identifies applicant `income`, `loan_amount`, and `loan_term` via regular expressions.
- **Financial Justification Engine**: Calculates total repayment capacity over the loan term and determines whether the requested loan amount is financially justified.
- **REST API**: Built on FastAPI with automatic interactive API docs.

---

## Prerequisites

1. **Python 3.10+**
2. **Tesseract OCR**:
   - On Windows, install Tesseract OCR (e.g. into `C:\Program Files\Tesseract-OCR\tesseract.exe`).
   - On Linux: `sudo apt install tesseract-ocr`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rahulreddy077/DocuJustify.git
   cd DocuJustify
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

Start the FastAPI application with Uvicorn:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

- Interactive API documentation (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative API documentation (ReDoc): `http://127.0.0.1:8000/redoc`

---

## API Usage

### `POST /analyze-document`

Upload a document to extract loan parameters and generate a financial justification report.

**Request:**
- `Content-Type`: `multipart/form-data`
- `file`: Document file (`.png`, `.jpg`, `.jpeg`, `.pdf`, `.csv`, `.txt`)

**Response Example:**
```json
{
  "filename": "form_0.png",
  "extracted_fields": {
    "income": 50000,
    "loan_amount": 100000,
    "loan_term": 5
  },
  "justification": "The applicant's annual income is 50000. Over 5 years, total income becomes 250000. The requested loan amount is 100000, which is within repayment capacity. Hence, the document is financially justified."
}
```

---

## Dataset

Sample loan documents across various formats are provided in `loan_dataset/` for testing positive and negative loan justification cases.
