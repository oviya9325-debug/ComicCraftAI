from __future__ import annotations

from pathlib import Path

from app.models import ComicPanel, ComicStory


def build_comic_layout(
    story: ComicStory,
    image_paths: list[str | Path],
) -> list[ComicPanel]:

    if len(story.panels) != len(image_paths):
        raise ValueError(
            f"Panel/image count mismatch: "
            f"{len(story.panels)} panels vs "
            f"{len(image_paths)} images."
        )

    layout: list[ComicPanel] = []

    for panel, image_path in zip(
        story.panels,
        image_paths,
    ):

        path = Path(image_path)

        layout.append(
            ComicPanel(
                panel_number=panel.panel_number,
                title=panel.title,
                image_url=f"/static/panels/{path.name}",
                scene_description=panel.scene_description,
                caption=panel.caption,
                narration=panel.narration,
                dialogue=panel.dialogue,
                image_prompt=panel.image_prompt,
            )
        )

    return layout