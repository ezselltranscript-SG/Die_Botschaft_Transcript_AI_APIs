from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from app.services.pdf_processor import pdf_to_images, split_pdf
from app.core.utils import validate_file_extension, cleanup_files
from app.core.config import STATIC_DIR
import os
import zipfile

router = APIRouter()

@router.post("/convert-to-images")
async def convert_pdf(
    file: UploadFile = File(...), 
    format: str = "png"
):
    validate_file_extension(file.filename, [".pdf"])
    
    try:
        pdf_bytes = await file.read()
        zip_buffer = pdf_to_images(pdf_bytes, format)
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=converted_images.zip"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/split")
async def split_pdf_endpoint(file: UploadFile = File(...)):
    validate_file_extension(file.filename, [".pdf"])
    
    try:
        # Save uploaded file
        upload_path = os.path.join(STATIC_DIR, "pdf_uploads", file.filename)
        with open(upload_path, "wb") as f:
            f.write(await file.read())
        
        # Split PDF
        output_files = split_pdf(upload_path, os.path.join(STATIC_DIR, "pdf_output"))
        
        # Create ZIP
        zip_path = os.path.join(STATIC_DIR, "zips", "split_pdf.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
        
        # Cleanup & return
        cleanup_files(upload_path, *output_files)
        return FileResponse(zip_path, filename="split_pdf.zip")
    
    except Exception as e:
        cleanup_files(upload_path)
        raise HTTPException(status_code=500, detail=str(e))