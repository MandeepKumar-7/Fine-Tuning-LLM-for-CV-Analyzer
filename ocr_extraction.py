
from pdf2image import convert_from_path, convert_from_bytes
import pytesseract
from PIL import Image
import argparse
import io
import sys

def extract_text_from_pdf_file(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a PDF via OCR.")
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("--out", default=None, help="Optional output .txt path")
    args = parser.parse_args()

    text = extract_text_from_pdf_file(args.pdf)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
