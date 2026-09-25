from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(
        min_length=3,
        max_length=3000,
    )

    character_name: str = Field(
        default="Hero",
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        default="enchanted forest",
        min_length=1,
        max_length=200,
    )

    tone: str = Field(
        default="dramatic",
        min_length=1,
        max_length=80,
    )

    art_style: str = Field(
        default="comic book",
        min_length=1,
        max_length=100,
    )

    panel_count: int = Field(
        default=5,
        ge=1,
        le=8,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    image_prompt: str


class ComicOutline(BaseModel):
    panels: list[PanelOutline]


class PanelStory(BaseModel):
    panel_number: int = Field(ge=1)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)
    image_prompt: str


class ComicStory(BaseModel):
    title: str
    panels: list[PanelStory]


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    scene_description: str
    caption: str
    narration: str
    dialogue: list[str] = Field(default_factory=list)
    image_prompt: str


class GenerateResponse(BaseModel):
    title: str
    panels: list[ComicPanel]
    pdf_url: str