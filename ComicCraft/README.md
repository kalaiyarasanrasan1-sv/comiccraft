# ComicCraft — AI Comic Story Creator

ComicCraft is a FastAPI web application based on the supplied project documentation. It accepts a story prompt, character, setting, tone, art style and panel count, then generates a panel outline, narration/dialogue, illustrations and a downloadable PDF.

## Architecture

Browser → FastAPI/Jinja2 → Gemini outline → Gemini story → Hugging Face image generation → layout builder → FPDF PDF export.

## Project structure

```text
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── schemas.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   └── export_success.html
├── static/
│   ├── css/style.css
│   ├── panels/
│   └── exports/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Windows / VS Code setup

1. Install Python 3.11 or newer.
2. Open this folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.venv\Scripts\Activate.ps1
```

6. Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env`.

8. Add your Gemini and Hugging Face tokens.

9. Run:

```powershell
uvicorn app.main:app --reload
```

10. Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## No API keys? Test the complete UI first

In `.env`:

```env
USE_MOCK_AI=true
```

Then restart Uvicorn. The application will create offline placeholder images and sample text while exercising the same routes, templates, layout and PDF export.

## AI mode

Set:

```env
USE_MOCK_AI=false
GEMINI_API_KEY=...
HF_TOKEN=...
```

The code uses the current Google GenAI Python SDK and Hugging Face InferenceClient. Model IDs are environment variables so they can be changed without editing Python.

## API example

POST `/generate-comic/json`:

```json
{
  "story_prompt": "A brave fox discovers a hidden portal in an enchanted forest.",
  "character_name": "Arin",
  "setting": "Enchanted Forest",
  "tone": "Adventure",
  "art_style": "Comic book",
  "panels": 5
}
```

## Testing checklist

1. `/health` returns `{"status":"ok",...}`.
2. Home page loads.
3. Submit a comic with `USE_MOCK_AI=true`.
4. Confirm all panels render.
5. Download the PDF.
6. Open `/docs` and test `/generate-comic/json`.
7. For AI mode, verify Gemini and Hugging Face credentials.
8. Test `/test-image?prompt=A%20cute%20fox`.

## Notes

The original document specifies Gemini 1.5 Flash/Pro and Stable Diffusion 1.5. Those model IDs are kept conceptually in the architecture, but this implementation makes model selection configurable because model availability changes. The defaults use currently configurable Gemini and Hugging Face models. This also avoids requiring a large local PyTorch/Stable Diffusion installation on a typical student laptop.

Never commit `.env` or API tokens to GitHub.
