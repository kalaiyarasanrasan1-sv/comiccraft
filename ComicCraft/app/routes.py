from fastapi import APIRouter, Form, HTTPException, Request
from .schemas import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf
from .config import PANELS

router = APIRouter()

@router.get("/")
async def home(request: Request):
    from .main import templates
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request, "panels": PANELS})

def generate_complete_comic(data: PromptRequest):
    outline = generate_outline(data.story_prompt, data.character_name, data.setting, data.tone, data.art_style, data.panels)
    story = generate_story(outline, data.character_name, data.tone)
    image_paths = [generate_image(panel.image_prompt, panel.panel_number) for panel in outline.panels]
    layout = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(layout)
    return layout, pdf_path

@router.post("/generate")
async def generate(request: Request, story_prompt: str = Form(...), character_name: str = Form(...), setting: str = Form(...), tone: str = Form(...), art_style: str = Form(...), panels: int = Form(PANELS)):
    try:
        data = PromptRequest(story_prompt=story_prompt.strip(), character_name=character_name.strip(), setting=setting.strip(), tone=tone.strip(), art_style=art_style.strip(), panels=panels)
        layout, pdf_path = generate_complete_comic(data)
        from .main import templates
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={"request": request, "layout": layout, "pdf_path": pdf_path})
    except Exception as error:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {error}")

@router.post("/generate-comic/json")
async def generate_json(data: PromptRequest):
    try:
        layout, pdf_path = generate_complete_comic(data)
        return {"success": True, "layout": layout, "pdf_path": pdf_path}
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {error}")

@router.get("/export-success")
async def export_success(request: Request, pdf: str = ""):
    from .main import templates
    return templates.TemplateResponse(request=request, name="export_success.html", context={"request": request, "pdf_path": pdf})

@router.get("/test-image")
async def test_image(prompt: str = "A cute fox hero in an enchanted forest, comic book art"):
    try:
        from .config import HF_TOKEN, USE_MOCK_AI
        image_path = generate_image(prompt, 1)
        return {"success": True, "image_path": image_path, "hf_token_configured": bool(HF_TOKEN), "use_mock_ai": USE_MOCK_AI}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
