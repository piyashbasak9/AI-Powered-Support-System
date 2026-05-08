import io
import pdfplumber
from PIL import Image

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_image(file_bytes):
    from PIL import Image
    image = Image.open(io.BytesIO(file_bytes))
    # Note: pytesseract required for real OCR
    return "Text extraction from images requires pytesseract"

def process_uploaded_file(file_obj):
    content = file_obj.read()
    ext = file_obj.name.split('.')[-1].lower()
    
    if ext == 'pdf':
        extracted_text = extract_text_from_pdf(content)
    else:
        extracted_text = extract_text_from_image(content)
    
    return {
        "extracted_text": extracted_text,
        "file_info": {"filename": file_obj.name, "size": file_obj.size, "type": ext}
    }