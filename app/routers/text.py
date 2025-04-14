# app/routers/text.py
from fastapi import APIRouter, HTTPException
from app.services.spellcheck import correct_text

router = APIRouter()

@router.post("/correct")
async def correct_text_endpoint(text: str):
    try:
        corrected = correct_text(text)
        return {
            "original": text,
            "corrected": corrected,
            "source": "Supabase towns table"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text: {str(e)}"
        )