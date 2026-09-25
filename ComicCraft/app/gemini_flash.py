import json
import requests

from .config import GEMINI_API_KEY, GEMINI_OUTLINE_MODEL, USE_MOCK_AI
from .schemas import ComicOutline


def create_mock_outline(prompt, character, setting, tone, art_style, panels):
    return ComicOutline(
        panels=[
            {
                "panel_number": i,
                "title": f"Panel {i}",
                "scene_description": (
                    f"{character} continues the {tone.lower()} "
                    f"adventure in {setting}."
                ),
                "image_prompt": (
                    f"{character} in {setting}, "
                    f"{art_style} comic art, panel {i}"
                ),
            }
            for i in range(1, panels + 1)
        ]
    )


def generate_outline(
    prompt,
    character,
    setting,
    tone,
    art_style,
    panels
):
    # Mock mode
    if USE_MOCK_AI or not GEMINI_API_KEY:
        print("[ComicCraft] Using mock outline")
        return create_mock_outline(
            prompt,
            character,
            setting,
            tone,
            art_style,
            panels
        )

    model_name = GEMINI_OUTLINE_MODEL

    print(f"[ComicCraft] Using Gemini model: {model_name}")

    instruction = f"""
Create a {panels}-panel comic outline.

Story prompt: {prompt}
Main character: {character}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

For every panel provide:
- panel_number
- title
- scene_description
- image_prompt

Keep the character and story consistent across all panels.

Return ONLY valid JSON in this exact format:

{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "Panel title",
      "scene_description": "Scene description",
      "image_prompt": "Detailed image generation prompt"
    }}
  ]
}}
"""

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model_name}:generateContent"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": instruction
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "responseMimeType": "application/json"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    try:
        print("[ComicCraft] Sending direct Gemini API request...")

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=120
        )

        print(
            f"[ComicCraft] Gemini HTTP status: "
            f"{response.status_code}"
        )

        if response.status_code != 200:
            print(
                "[ComicCraft] Gemini API error:"
            )
            print(response.text)

            raise RuntimeError(
                f"Gemini API returned HTTP "
                f"{response.status_code}: {response.text}"
            )

        data = response.json()

        candidates = data.get("candidates", [])

        if not candidates:
            raise RuntimeError(
                "Gemini returned no candidates."
            )

        text = (
            candidates[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        if not text:
            raise RuntimeError(
                "Gemini returned empty response."
            )

        print("[ComicCraft] Gemini response received")

        # Remove accidental markdown fences
        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        parsed = json.loads(text)

        return ComicOutline.model_validate(parsed)

    except requests.RequestException as error:
        print("[ComicCraft] Network error:")
        print(error)

        raise RuntimeError(
            f"Gemini network request failed: {error}"
        )

    except json.JSONDecodeError as error:
        print("[ComicCraft] Invalid JSON from Gemini:")
        print(text if "text" in locals() else "")

        raise RuntimeError(
            f"Gemini returned invalid JSON: {error}"
        )

    except Exception as error:
        print("[ComicCraft] Gemini request failed:")
        print(error)

        raise RuntimeError(
            f"Gemini outline generation failed: {error}"
        )