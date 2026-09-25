from typing import List
from pydantic import BaseModel, Field

class PanelOutline(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    image_prompt: str

class ComicOutline(BaseModel):
    panels: List[PanelOutline]

class PanelStory(BaseModel):
    panel_number: int
    caption: str
    narration: str
    dialogue: str

class ComicStory(BaseModel):
    panels: List[PanelStory]

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=5, max_length=2000)
    character_name: str = Field(min_length=1, max_length=100)
    setting: str = Field(min_length=1, max_length=100)
    tone: str = Field(min_length=1, max_length=50)
    art_style: str = Field(min_length=1, max_length=80)
    panels: int = Field(default=5, ge=3, le=8)
