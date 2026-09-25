from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent
(BASE_DIR / "static" / "panels").mkdir(parents=True, exist_ok=True)
(BASE_DIR / "static" / "exports").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate personalized 5-panel comics with Gemini and Hugging Face.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft"}
