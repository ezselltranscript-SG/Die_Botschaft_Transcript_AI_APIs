# app/services/image_processor.py
from PIL import Image
import zipfile
import os

def crop_image(image_path: str, output_dir: str) -> str:
    """Crop image into header and body sections."""
    img = Image.open(image_path)
    width, height = img.size
    
    # Define crop regions
    header = img.crop((0, int(height*0.12), width, int(height*0.30)))
    body = img.crop((0, int(height*0.31), width, height))
    
    # Save crops
    header_path = os.path.join(output_dir, "header.png")
    body_path = os.path.join(output_dir, "body.png")
    header.save(header_path)
    body.save(body_path)
    
    # Create ZIP
    zip_path = os.path.join(output_dir, "cropped_images.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(header_path, "header.png")
        zipf.write(body_path, "body.png")
    
    return zip_path