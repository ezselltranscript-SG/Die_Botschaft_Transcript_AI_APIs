from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile
import os
from app.core.config import STATIC_DIR

def pdf_to_images(pdf_bytes: bytes, original_filename: str = "document", format: str = "png") -> io.BytesIO:
    """Convert PDF pages to images (PNG/JPEG), keeping proper file naming."""
    images = convert_from_bytes(pdf_bytes)
    zip_buffer = io.BytesIO()
    
    # Remove extension (.pdf) if present
    base_name = os.path.splitext(original_filename)[0]

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for i, image in enumerate(images):
            img_io = io.BytesIO()
            image.save(img_io, format=format.upper())
            img_io.seek(0)
            filename = f"{base_name}_Part{i+1}.{format}"
            zip_file.writestr(filename, img_io.read())
    
    zip_buffer.seek(0)
    return zip_buffer

def split_pdf(pdf_path: str, output_dir: str) -> list:
    """Split PDF into multiple files (2 pages per file), with correct naming."""
    reader = PdfReader(pdf_path)
    output_files = []

    # Get base name without extension
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    for i in range(0, len(reader.pages), 2):
        writer = PdfWriter()
        writer.add_page(reader.pages[i])
        if i + 1 < len(reader.pages):
            writer.add_page(reader.pages[i + 1])

        output_filename = f"{base_name}_Part{(i // 2) + 1}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, "wb") as f:
            writer.write(f)
        output_files.append(output_path)
    
    return output_files
