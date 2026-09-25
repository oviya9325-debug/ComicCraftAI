from __future__ import annotations

from app.models import ComicOutline, ComicStory, PanelStory


def generate_story(
    outline: ComicOutline,
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
) -> ComicStory:

    panels = []

    for panel in outline.panels:
        number = panel.panel_number

        if number == 1:
            caption = "A mysterious adventure begins."
            narration = (
                f"{character_name} enters the {setting} and discovers "
                "that something is wrong."
            )
            dialogue = [
                f"{character_name}: Something strange is happening here!"
            ]

        elif number == len(outline.panels):
            caption = "The adventure reaches its hopeful ending."
            narration = (
                f"{character_name} faces the final challenge and "
                "finds a peaceful solution."
            )
            dialogue = [
                f"{character_name}: The light has returned!"
            ]

        else:
            caption = f"The adventure continues in the {setting}."
            narration = (
                f"{character_name} continues forward, following clues "
                "and overcoming the next challenge."
            )
            dialogue = [
                f"{character_name}: I have to keep going."
            ]

        panels.append(
            PanelStory(
                panel_number=number,
                title=panel.title,
                scene_description=panel.scene_description,
                caption=caption,
                narration=narration,
                dialogue=dialogue,
                image_prompt=panel.image_prompt,
            )
        )

    return ComicStory(
        title=f"The Adventure of {character_name}",
        panels=panels,
    )