from __future__ import annotations

from app.models import ComicOutline, PanelOutline


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panel_count: int = 5,
) -> ComicOutline:

    panels = []

    for i in range(1, panel_count + 1):

        if i == 1:
            scene = (
                f"{character_name} discovers something unusual "
                f"in the {setting}."
            )

        elif i == panel_count:
            scene = (
                f"{character_name} solves the mystery and brings "
                f"a hopeful ending to the adventure."
            )

        else:
            scene = (
                f"{character_name} continues the adventure through "
                f"the {setting}, facing a new challenge."
            )

        image_prompt = (
            f"{character_name}, {scene} "
            f"Comic book art, {art_style}, {tone} mood, "
            f"cinematic composition, detailed environment, "
            f"dramatic lighting, consistent character appearance."
        )

        panels.append(
            PanelOutline(
                panel_number=i,
                title=f"Panel {i}",
                scene_description=scene,
                image_prompt=image_prompt,
            )
        )

    return ComicOutline(panels=panels)