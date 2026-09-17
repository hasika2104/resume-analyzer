import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile

from app.config import get_settings

settings = get_settings()


async def save_upload_file(file: UploadFile) -> tuple[str, str, str]:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Supported: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    return unique_name, file_path, ext.lstrip(".")
