from typing import Annotated

from fastapi import FastAPI, File

app = FastAPI()


@app.get('/health_check/')
def health_check():
    return {"message": "Healthy!"}


@app.post('/capture/')
def capture(image: Annotated[bytes, File()]):
    print(f'{len(image)=}')
    return {'status': 'success'}
