from fastapi import FastAPI

app = FastAPI()


@app.get('/health_check/')
def health_check():
    return {"message": "Healthy!"}
