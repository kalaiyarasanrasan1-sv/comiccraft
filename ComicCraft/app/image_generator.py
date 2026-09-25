from pathlib import Path
import re
from PIL import Image, ImageDraw
from huggingface_hub import InferenceClient
from .config import HF_TOKEN, HF_IMAGE_MODEL, HF_PROVIDER, USE_MOCK_AI

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "static" / "panels"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def safe_filename(text):
    text = re.sub(r"[^a-zA-Z0-9_-]+", "-", text).strip("-")
    return (text or "panel")[:60]


def create_mock_image(prompt, path, panel_number):
    image = Image.new("RGB", (1024, 1024), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 40, 984, 984), outline="black", width=8)
    draw.text((70, 70), f"ComicCraft - Panel {panel_number}", fill="black")
    draw.text((70, 140), "Offline Preview", fill="black")
    draw.text((70, 210), prompt[:250], fill="black")
    image.save(path, format="PNG")


def generate_image(prompt: str, panel_number: int):
    filename = f"panel-{panel_number}-{safe_filename(prompt)}.png"
    path = OUTPUT_DIR / filename
    if USE_MOCK_AI or not HF_TOKEN:
        create_mock_image(prompt, path, panel_number)
        return f"/static/panels/{filename}"
    try:
        client = InferenceClient(provider=HF_PROVIDER, api_key=HF_TOKEN)
        image = client.text_to_image(
            prompt=prompt,
            model=HF_IMAGE_MODEL,
            negative_prompt="blurry, distorted anatomy, extra limbs, duplicate character, watermark, logo, readable text"
        )
        image.save(str(path), format="PNG")
        if not path.exists() or path.stat().st_size == 0:
            raise RuntimeError(f"Image was not saved correctly: {path}")
        print(f"[ComicCraft] Image saved: {path}")
        return f"/static/panels/{filename}"
    except Exception as error:
        print(f"[ComicCraft] Image generation error: {error}")
        raise
