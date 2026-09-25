from __future__ import annotations

import hashlib
from pathlib import Path

from app.config import get_settings


def generate_image(
    image_prompt: str,
    panel_number: int,
) -> Path:

    settings = get_settings()

    if settings.image_provider != "huggingface":
        raise ValueError(
            "IMAGE_PROVIDER must be 'huggingface'."
        )

    if not settings.has_hf_token:
        raise RuntimeError(
            "HF_API_KEY is not configured."
        )

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        api_key=settings.hf_api_key,
        provider="auto",
    )

    seed_text = f"{panel_number}:{image_prompt}"

    seed = int(
        hashlib.sha256(
            seed_text.encode("utf-8")
        ).hexdigest()[:8],
        16,
    )

    prompt = (
        f"{image_prompt}. "
        "High quality comic book illustration, "
        "consistent character appearance, "
        "detailed environment, "
        "cinematic composition, "
        "dramatic lighting, "
        "vibrant colors, "
        "professional comic art."
    )

    image = client.text_to_image(
        prompt=prompt,
        model=settings.image_model_id,
        width=settings.image_width,
        height=settings.image_height,
        num_inference_steps=4,
        guidance_scale=0.0,
        seed=seed,
    )

    output_path = (
        settings.panels_dir
        / f"panel_{panel_number}.png"
    )

    image.save(
        output_path,
        format="PNG",
    )

    return output_path