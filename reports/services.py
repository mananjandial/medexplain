# from PyPDF2 import PdfReader

# def extract_text_from_file(file_path):
#     text = ""

#     if file_path.endswith('.pdf'):
#         reader = PdfReader(file_path)
#         for page in reader.pages:
#             text += page.extract_text() or ""

#     elif file_path.endswith('.txt'):
#         with open(file_path, 'r', encoding='utf-8') as f:
#             text = f.read()

#     return text.strip()
# old code till herer ####################################
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import os

def extract_text_from_file(file_path):
    extracted_text = ""
    ext = os.path.splitext(file_path)[1].lower()

    # PDF
    if ext == ".pdf":
        reader = PdfReader(file_path)
        for page in reader.pages:
            extracted_text += page.extract_text() or ""

    # TEXT
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            extracted_text = f.read()

    # IMAGE (OCR)
    elif ext in [".png", ".jpg", ".jpeg"]:
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)

    return extracted_text.strip()
