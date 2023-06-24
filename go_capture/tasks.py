import io
import os
from pathlib import Path

import firebase_admin
from celery import Celery
from django.conf import settings
from firebase_admin import credentials, messaging

from go_capture.sgf.process_image import process_image

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "go_capture.settings")

app = Celery("go_capture")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_FILE)
firebase_admin.initialize_app(cred)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.task
def process_image_task(image_filename, fcm_token):
    print(f"token: {fcm_token}")
    print(f"Processing {image_filename}")
    with open(image_filename, "rb") as image_file:
        sgf_buffer = io.StringIO()
        process_image(image_file, sgf_buffer)

    sgf_buffer.seek(0)
    sgf_data = sgf_buffer.read()
    print(sgf_data)
    message = messaging.Message(
        data={
            "sgf": sgf_data,
            "image_filename": Path(image_filename).name,
        },
        token=fcm_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print("Successfully sent message:", response)
