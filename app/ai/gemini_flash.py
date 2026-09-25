from __future__ import annotations

import time

from app.config import get_settings
from app.models import ComicOutline


def _client():
    from google import genai

    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panel_count: int = 5,
) -> ComicOutline:

    settings = get_settings()
    client = _client()

    prompt = f"""
Create a cohesive {panel_count}-panel comic outline.

USER STORY IDEA:
{story_prompt}

MAIN CHARACTER:
{character_name}

SETTING:
{setting}

TONE:
{tone}

VISUAL STYLE:
{art_style}

REQUIREMENTS:

- Return exactly {panel_count} panels.
- Keep the same main character visually consistent.
- Give every panel a short title.
- Give every panel a concise scene description.
- Give every panel a detailed image-generation prompt.
- The image prompt must describe:
  character appearance,
  environment,
  composition,
  camera angle,
  lighting,
  mood,
  and visual style.
- Do not put dialogue in the image prompt.
- Make the story have a clear beginning, middle, and ending.
- Maintain continuity between panels.
"""

    # Retry temporary Gemini 503 errors
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ComicOutline,
                    "temperature": 0.8,
                    "max_output_tokens": 3000,
                },
            )
            break

        except Exception as exc:
            error_text = str(exc)

            if "503" not in error_text and "UNAVAILABLE" not in error_text:
                raise

            if attempt == max_attempts - 1:
                raise RuntimeError(
                    "Gemini is temporarily unavailable after 3 attempts. "
                    "Please try again in a minute."
                ) from exc

            wait_seconds = 2 ** attempt
            time.sleep(wait_seconds)

    parsed = getattr(
        response,
        "parsed",
        None,
    )

    if isinstance(parsed, ComicOutline):
        return parsed

    text = getattr(
        response,
        "text",
        None,
    )

    if not text:
        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    return ComicOutline.model_validate_json(text)