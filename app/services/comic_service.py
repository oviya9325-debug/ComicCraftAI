from __future__ import annotations

from app.models import ComicPanel, PromptRequest
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout


def generate_comic(
    request: PromptRequest,
) -> tuple[str, list[ComicPanel], str]:

    # Step 1: Generate comic outline using Gemini
    outline = generate_outline(
        story_prompt=request.story_prompt,
        character_name=request.character_name,
        setting=request.setting,
        tone=request.tone,
        art_style=request.art_style,
        panel_count=request.panel_count,
    )

    # Step 2: Expand outline into full comic story
    story = generate_story(
        outline=outline,
        story_prompt=request.story_prompt,
        character_name=request.character_name,
        setting=request.setting,
        tone=request.tone,
        art_style=request.art_style,
    )

    # Step 3: Generate one image for every panel
    image_paths = []

    for panel in story.panels:

        image_path = generate_image(
            image_prompt=panel.image_prompt,
            panel_number=panel.panel_number,
        )

        image_paths.append(image_path)

    # Step 4: Build final comic layout
    layout = build_comic_layout(
        story,
        image_paths,
    )

    # Step 5: Export comic as PDF
    pdf_path = save_pdf(
        story.title,
        layout,
    )

    pdf_url = f"/static/exports/{pdf_path.name}"

    return story.title, layout, pdf_url