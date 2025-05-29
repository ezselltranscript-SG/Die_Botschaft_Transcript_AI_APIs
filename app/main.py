from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers import text, pdf, images

app = FastAPI(
    title="Die Botschaft Transcript API",
    description="Unified API for PDF, Image & Text Processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(text.router, prefix="/api/text", tags=["Text Processing"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["PDF Tools"])
app.include_router(images.router, prefix="/api/images", tags=["Image Tools"])

# Root route redirect to docs
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")