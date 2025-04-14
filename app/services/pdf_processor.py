from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile
import os
from app.core.config import STATIC_DIR

def pdf_to_images(pdf_bytes: bytes, format: str = "png") -> io.BytesIO:
    """Convert PDF pages to images (PNG/JPEG)."""
    images = convert_from_bytes(pdf_bytes)
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, image in enumerate(images):
            img_io = io.BytesIO()
            image.save(img_io, format=format.upper())
            img_io.seek(0)
            zip_file.writestr(f"page_{i+1}.{format}", img_io.read())
    
    zip_buffer.seek(0)
    return zip_buffer

def split_pdf(pdf_path: str, output_dir: str) -> list:
    """Split PDF into multiple files (2 pages per file)."""
    reader = PdfReader(pdf_path)
    output_files = []
    
    for i in range(0, len(reader.pages), 2):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        if i + 1 < len(reader.pages):
            writer.add_page(reader.pages[i + 1])
        
        output_path = os.path.join(output_dir, f"part_{(i//2)+1}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        output_files.append(output_path)
    
    return output_files