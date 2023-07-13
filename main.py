import io
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

from sgf.process_image import process_image

app = FastAPI()


@app.get('/health_check/')
def health_check():
    return {"message": "Healthy!"}


@app.post('/capture/')
def capture(image: Annotated[UploadFile, File()]):
    output_file = io.StringIO()
    process_image(image.file, output_file)
    output_file.seek(0)
    return {
        'sgf': output_file.read(),
        'image_filename': image.filename,
    }
