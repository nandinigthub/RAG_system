import fitz
import pdfplumber
import io

def extract_pdf_content(file_bytes: bytes):
    """Extracts raw text and images"""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    images = []

    for page_num, page in enumerate(doc):
        full_text += f"\nPage {page_num + 1}\n"
        full_text += page.get_text("text")

        for img_index, img in enumerate(page.get_images(full=True)):
            base_image = doc.extract_image(img[0])
            img_bytes = base_image["image"]
            images.append({
                "page": page_num + 1,
                "index": img_index,
                "image": img_bytes
            })

    return full_text, images

def extract_pdf_tables(file_bytes):
    """Extracts tables"""
    tables = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            page_tables = page.extract_tables()
            for table in page_tables:
                tables.append({
                    "page": i + 1,
                    "data": table
                })
    return tables

def parse_pdf(file):
    """Unified parsing: text, images, tables."""
    file_bytes = file.file.read()
    text, images = extract_pdf_content(file_bytes)
    tables = extract_pdf_tables(file_bytes)
    return text, tables, images
