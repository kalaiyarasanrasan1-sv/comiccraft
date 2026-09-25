import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

GEMINI_OUTLINE_MODEL = os.getenv("GEMINI_OUTLINE_MODEL", "gemini-2.5-flash")
GEMINI_STORY_MODEL = os.getenv("GEMINI_STORY_MODEL", "gemini-2.5-pro")
HF_IMAGE_MODEL = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
HF_PROVIDER = os.getenv("HF_PROVIDER", "auto")
PANELS = int(os.getenv("PANELS", "5"))
USE_MOCK_AI = os.getenv("USE_MOCK_AI", "false").lower() == "true"
APP_ENV = os.getenv("APP_ENV", "development")

if PANELS < 3 or PANELS > 8:
    PANELS = 5
