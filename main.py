import io
from enum import Enum
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, UploadFile, Form

import settings
from sgf.process_image import process_image
from tasks import process_image_task

app = FastAPI()


class Color(str, Enum):
    BLACK = "B"
    WHITE = "W"


@app.get("/health_check/")
def health_check():
    return {"message": "Healthy!"}


@app.post("/capture/")
def capture(
    image: Annotated[UploadFile, File()],
    to_play: Annotated[Color, Form()] = Color.BLACK,
):
    output_file = io.StringIO()
    process_image(image.file, output_file, to_play)
    output_file.seek(0)
    return {
        "sgf": output_file.read(),
        "image_filename": image.filename,
    }


@app.post("/capture_async/")
def capture_async(
    image: Annotated[UploadFile, File()],
    fcm_registration_token: Annotated[str, Form()],
    to_play: Annotated[Color, Form()] = Color.BLACK,
):
    filename = Path(image.filename)
    output_path = settings.IMAGES_DIR / filename
    with output_path.open("wb") as output_file:
        output_file.write(image.file.read())
    process_image_task.delay(
        str(output_path.absolute()), fcm_registration_token, to_play
    )
