from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, GEMINI_STORY_MODEL, USE_MOCK_AI
from .schemas import ComicStory, ComicOutline


def create_mock_story(outline, character, tone):
    panels = []
    for panel in outline.panels:
        panels.append({
            "panel_number": panel.panel_number,
            "caption": f"The {tone.lower()} adventure continues...",
            "narration": panel.scene_description,
            "dialogue": f"{character}: We have to keep going!"
        })
    return ComicStory(panels=panels)


def generate_story(outline, character, tone):
    if USE_MOCK_AI or not GEMINI_API_KEY:
        return create_mock_story(outline, character, tone)

    client = genai.Client(api_key=GEMINI_API_KEY)
    schema = {
        "type": "object",
        "properties": {
            "panels": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "panel_number": {"type": "integer"},
                        "caption": {"type": "string"},
                        "narration": {"type": "string"},
                        "dialogue": {"type": "string"}
                    },
                    "required": ["panel_number", "caption", "narration", "dialogue"]
                }
            }
        },
        "required": ["panels"]
    }

    outline_text = "\n".join(
        f"""
Panel {panel.panel_number}
Title: {panel.title}
Scene: {panel.scene_description}
Image: {panel.image_prompt}
"""
        for panel in outline.panels
    )

    prompt = f"""
You are a professional comic writer.
Main character: {character}
Tone: {tone}
Comic outline:
{outline_text}

Expand the outline into a complete comic story.
For every panel generate caption, narration and character dialogue.
Keep the same story and character personality. Keep dialogue short and natural.
Return ONLY JSON.
"""

    models_to_try = [GEMINI_STORY_MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]
    last_error = None
    for model_name in models_to_try:
        try:
            print(f"[ComicCraft] Trying story model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.9
                )
            )
            print(f"[ComicCraft] Story success: {model_name}")
            return ComicStory.model_validate_json(response.text)
        except Exception as error:
            last_error = error
            print(f"[ComicCraft] Story failed: {model_name}")
            print(error)
            continue

    print("[ComicCraft] Gemini story unavailable. Using local story fallback.")
    return create_mock_story(outline, character, tone)
