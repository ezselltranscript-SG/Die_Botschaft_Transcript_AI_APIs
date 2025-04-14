# app/services/spellcheck.py
import re
from typing import List
from fuzzywuzzy import fuzz
from app.core.config import supabase

def fetch_town_names() -> List[str]:
    """
    Obtiene nombres de ciudades desde Supabase (tabla: 'towns')
    """
    response = supabase.table("towns").select("name").execute() 
    if response.data:
        return [entry["name"] for entry in response.data]  
    return []

def correct_text(text: str, threshold: int = 85) -> str:
    """
    Corrige el texto comparando con nombres de ciudades
    """
    towns = fetch_town_names()  
    words = re.findall(r"\b\w+\b", text)
    corrected_words = []

    for word in words:
        best_match = max(
            towns,
            key=lambda town: fuzz.ratio(word.lower(), town.lower())
        )
        similarity = fuzz.ratio(word.lower(), best_match.lower())
        corrected_words.append(best_match if similarity >= threshold else word)

    return " ".join(corrected_words)