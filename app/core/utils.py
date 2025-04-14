import os
from fastapi import HTTPException
from typing import Optional

def validate_file_extension(filename: str, allowed_extensions: list) -> None:
    """Check if file has a valid extension."""
    if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400, 
            detail=f"File type not allowed. Use: {', '.join(allowed_extensions)}"
        )

def cleanup_files(*file_paths: str) -> None:
    """Delete temporary files after processing."""
    for path in file_paths:
        if os.path.exists(path):
            os.remove(path)