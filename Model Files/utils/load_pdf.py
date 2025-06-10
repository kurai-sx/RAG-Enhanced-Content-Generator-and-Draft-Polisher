# utils/load_pdf.py

from PyPDF2 import PdfReader

def load_banned_keywords_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
    return full_text
