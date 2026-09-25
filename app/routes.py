from __future__ import annotations

from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import get_settings

from app.models import (
    GenerateResponse,
    PromptRequest,
)

from app.services.comic_service import (
    generate_comic,
)

from app.services.image_generator import (
    generate_image,
)


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


def _request_from_form(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
    panel_count: int,
) -> PromptRequest:

    return PromptRequest(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
        panel_count=panel_count,
    )


@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "default_panel_count":
                settings.default_panel_count,

            "max_panel_count":
                settings.max_panel_count,

            "image_provider":
                settings.image_provider,
        },
    )


@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),

    panel_count: int = Form(5),
):

    try:

        payload = _request_from_form(
            story_prompt,
            character_name,
            setting,
            tone,
            art_style,
            panel_count,
        )

        title, layout, pdf_url = (
            generate_comic(
                payload
            )
        )

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
         context={
    "title": title,
    "panels": layout,
    "pdf_url": pdf_url,
},
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            status_code=500,
            context={
                "default_panel_count":
                    settings.default_panel_count,

                "max_panel_count":
                    settings.max_panel_count,

                "image_provider":
                    settings.image_provider,

                "error": str(exc),
            },
        )


@router.post(
    "/generate-comic/json",
    response_model=GenerateResponse,
)
async def generate_comic_json(
    payload: PromptRequest,
):

    try:

        title, layout, pdf_url = (
            generate_comic(
                payload
            )
        )

        return GenerateResponse(
            context={
    "title": title,
    "panels": layout,
    "pdf_url": pdf_url,
},
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    filename: str | None = None,
):

    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "filename": filename,
        },
    )


@router.get(
    "/download/{filename}"
)
async def download_pdf(
    filename: str,
):

    safe_name = Path(
        filename
    ).name

    if (
        safe_name != filename
        or not safe_name.lower().endswith(
            ".pdf"
        )
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid PDF filename.",
        )

    path = (
        settings.exports_dir
        / safe_name
    )

    if not path.is_file():

        raise HTTPException(
            status_code=404,
            detail="PDF not found.",
        )

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=safe_name,
    )


@router.post(
    "/test-image",
    response_class=HTMLResponse,
)
async def test_image(
    request: Request,
    image_prompt: str = Form(...),
):

    try:

        path = generate_image(
            image_prompt,
            panel_number=999,
        )

        filename = Path(
            path
        ).name

        image_url = (
            "/static/panels/"
            + filename
        )

        return templates.TemplateResponse(
            request=request,
            name="test_image.html",
            context={
                "image_url": image_url,
                "image_prompt": image_prompt,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="test_image.html",
            status_code=500,
            context={
                "error": str(exc),
                "image_prompt": image_prompt,
            },
        )


@router.get("/health")
async def health():

    return JSONResponse(
        {
            "status": "ok",
            "gemini_configured":
                settings.has_gemini_key,

            "image_provider":
                settings.image_provider,

            "huggingface_token_configured":
                settings.has_hf_token,
        }
    )