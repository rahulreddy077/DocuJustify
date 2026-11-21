import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from fastapi import FastAPI, File, UploadFile
import pytesseract
from PIL import Image
import pdfplumber
import pandas as pd
import re
import shutil
import os

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------
# TEXT EXTRACTION FUNCTION
# -------------------------

def extract_text_from_file(path):

    if path.endswith(".txt"):
        with open(path, "r") as f:
            return f.read()

    elif path.endswith(".csv"):
        df = pd.read_csv(path)
        return df.to_string()

    elif path.endswith(".pdf"):
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text()
        return text

    elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
        image = Image.open(path)
        text = pytesseract.image_to_string(image)
        return text

    else:
        return ""


# -------------------------
# FIELD EXTRACTION FUNCTION
# -------------------------

def extract_loan_fields(text):

    income = re.search(r"Income[:\s]+(\d+)", text, re.IGNORECASE)
    loan = re.search(r"Loan Amount[:\s]+(\d+)", text, re.IGNORECASE)
    years = re.search(r"Loan Term[:\s]+(\d+)", text, re.IGNORECASE)

    return {
        "income": int(income.group(1)) if income else None,
        "loan_amount": int(loan.group(1)) if loan else None,
        "loan_term": int(years.group(1)) if years else None
    }


# -------------------------
# JUSTIFICATION ENGINE
# -------------------------

def justify_loan(fields):

    income = fields["income"]
    loan = fields["loan_amount"]
    years = fields["loan_term"]

    if income is None:
        return "Income field not found in document."

    if loan is None:
        return "Loan amount field not found in document."

    if years is None:
        return "Loan term field not found in document."

    repayment_capacity = income * years

    if loan <= repayment_capacity:

        return (
            f"The applicant's annual income is {income}. "
            f"Over {years} years, total income becomes {repayment_capacity}. "
            f"The requested loan amount is {loan}, which is within repayment capacity. "
            f"Hence, the document is financially justified."
        )

    else:

        return (
            f"The applicant's annual income is {income}. "
            f"Over {years} years, total income becomes {repayment_capacity}. "
            f"The requested loan amount is {loan}, which exceeds repayment capacity. "
            f"Hence, this loan request may not be financially feasible."
        )


# -------------------------
# API ENDPOINT
# -------------------------

@app.post("/analyze-document")
async def analyze_document(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_file(file_path)

    fields = extract_loan_fields(text)

    justification = justify_loan(fields)

    return {
        "filename": file.filename,
        "extracted_fields": fields,
        "justification": justification
    }
