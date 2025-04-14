import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# File storage paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Create directories if they don't exist
os.makedirs(os.path.join(STATIC_DIR, "pdf_uploads"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "pdf_output"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "zips"), exist_ok=True)