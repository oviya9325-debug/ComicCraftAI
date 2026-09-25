from __future__ import annotations

from pathlib import Path

from fpdf import FPDF

from app.config import get_settings
from app.models import ComicPanel


def save_pdf(title: str, panels: list[ComicPanel]) -> Path:
    settings = get_settings()

    output_dir = settings.exports_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_title = "".join(
        character
        if character.isalnum() or character in " _-"
        else "_"
        for character in title
    ).strip()

    if not safe_title:
        safe_title = "comic"

    pdf_path = output_dir / f"{safe_title}.pdf"

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15,
    )

    for panel in panels:

        pdf.add_page()

        # Comic title
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(
            0,
            10,
            title,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(3)

        # Panel title
        pdf.set_font("Helvetica", "B", 13)
        pdf.multi_cell(
            0,
            8,
            f"Panel {panel.panel_number}: {panel.title}",
            new_x="LMARGIN",
            new_y="NEXT",
        )

        pdf.ln(2)

        # Panel image
        image_path = _get_image_path(
            panel.image_url,
            settings,
        )

        if image_path is None:
            raise FileNotFoundError(
                f"Comic panel image not found: "
                f"{panel.image_url}"
            )

        if not image_path.exists():
            raise FileNotFoundError(
                f"Comic panel image file does not exist: "
                f"{image_path}"
            )

        pdf.image(
            str(image_path),
            x=15,
            y=None,
            w=180,
        )

        pdf.ln(5)

        # Caption
        if panel.caption:
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(
                0,
                7,
                f"Caption: {panel.caption}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.ln(2)

        # Narration
        if panel.narration:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(
                0,
                6,
                f"Narration: {panel.narration}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.ln(2)

        # Dialogue
        if panel.dialogue:
            pdf.set_font("Helvetica", "B", 10)
            pdf.multi_cell(
                0,
                6,
                "Dialogue:",
                new_x="LMARGIN",
                new_y="NEXT",
            )

            pdf.set_font("Helvetica", "", 10)

            for line in panel.dialogue:
                pdf.multi_cell(
                    0,
                    6,
                    f"- {line}",
                    new_x="LMARGIN",
                    new_y="NEXT",
                )

    pdf.output(str(pdf_path))

    return pdf_path


def _get_image_path(
    image_url: str,
    settings,
) -> Path | None:

    if not image_url:
        return None

    filename = Path(
        image_url.split("?")[0]
    ).name

    image_path = (
        settings.panels_dir / filename
    )

    return image_path