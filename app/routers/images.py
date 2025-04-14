from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.services.image_processor import crop_image 
from app.core.utils import validate_file_extension, cleanup_files
from app.core.config import STATIC_DIR
import os

router = APIRouter()

@router.post("/crop")
async def crop_image_endpoint(file: UploadFile = File(...)):
    validate_file_extension(file.filename, [".png", ".jpg", ".jpeg"])
    
    try:
        # Save uploaded image
        upload_path = os.path.join(STATIC_DIR, "pdf_uploads", file.filename)
        with open(upload_path, "wb") as f:
            f.write(await file.read())
        
        # Process and get ZIP path
        zip_path = crop_image(upload_path, os.path.join(STATIC_DIR, "zips"))
        
        # Cleanup & return
        cleanup_files(upload_path)
        return FileResponse(zip_path, filename="cropped_images.zip")
    
    except Exception as e:
        cleanup_files(upload_path)
        raise HTTPException(status_code=500, detail=str(e))