from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _int(value: str | None, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _float(value: str | None, default: float) -> float:
    try:
        return float(value) if value is not None else default
    except (TypeError, ValueError):
        return default


class Settings:

    def __init__(self) -> None:

        self.app_name = os.getenv(
            "APP_NAME",
            "ComicCraft",
        )

        self.debug = _bool(
            os.getenv("DEBUG"),
            True,
        )

        self.gemini_api_key = os.getenv(
            "GEMINI_API_KEY",
            "",
        ).strip()

        self.gemini_outline_model = os.getenv(
            "GEMINI_OUTLINE_MODEL",
            "gemini-3.8-flash",
        ).strip()

        self.gemini_story_model = os.getenv(
            "GEMINI_STORY_MODEL",
            "gemini-3.1-pro-preview",
        ).strip()

        self.hf_api_key = (
            os.getenv("HF_API_KEY")
            or os.getenv("HUGGINGFACE_HUB_TOKEN")
            or ""
        ).strip()

        self.image_provider = os.getenv(
            "IMAGE_PROVIDER",
            "placeholder",
        ).strip().lower()

        self.image_model_id = os.getenv(
            "IMAGE_MODEL_ID",
            "stable-diffusion-v1-5/stable-diffusion-v1-5",
        ).strip()

        self.image_steps = _int(
            os.getenv("IMAGE_STEPS"),
            20,
        )

        self.image_width = _int(
            os.getenv("IMAGE_WIDTH"),
            512,
        )

        self.image_height = _int(
            os.getenv("IMAGE_HEIGHT"),
            512,
        )

        self.image_guidance_scale = _float(
            os.getenv("IMAGE_GUIDANCE_SCALE"),
            7.5,
        )

        self.image_device = os.getenv(
            "IMAGE_DEVICE",
            "auto",
        ).strip().lower()

        self.default_panel_count = _int(
            os.getenv("DEFAULT_PANEL_COUNT"),
            5,
        )

        self.max_panel_count = _int(
            os.getenv("MAX_PANEL_COUNT"),
            8,
        )

        self.max_prompt_length = _int(
            os.getenv("MAX_PROMPT_LENGTH"),
            3000,
        )

        self.templates_dir = BASE_DIR / "templates"

        self.static_dir = BASE_DIR / "static"

        self.panels_dir = self.static_dir / "panels"

        self.exports_dir = self.static_dir / "exports"

        self.panels_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.exports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @property
    def has_gemini_key(self) -> bool:
        return bool(self.gemini_api_key)

    @property
    def has_hf_token(self) -> bool:
        return bool(self.hf_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()