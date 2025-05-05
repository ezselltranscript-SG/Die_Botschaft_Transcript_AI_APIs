# app/services/image_processor.py
from PIL import Image
import zipfile
import os
import uuid

def crop_image(image_path: str, base_output_dir: str) -> str:
    """Crop image into header and body, and zip them in a unique folder."""
    unique_dir = os.path.join(base_output_dir, str(uuid.uuid4()))
    os.makedirs(unique_dir, exist_ok=True)

    img = Image.open(image_path)
    width, height = img.size

    header = img.crop((0, int(height*0.12), width, int(height*0.30)))
    body = img.crop((0, int(height*0.31), width, height))

    header_path = os.path.join(unique_dir, "header.png")
    body_path = os.path.join(unique_dir, "body.png")
    header.save(header_path)
    body.save(body_path)

    zip_path = os.path.join(unique_dir, "cropped_images.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.write(header_path, "header.png")
        zipf.write(body_path, "body.png")

    return zip_path
