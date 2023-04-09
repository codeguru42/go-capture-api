import os
from pathlib import Path

from celery import Celery
from django.conf import settings

from go_capture.sgf.process_image import process_image

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'go_capture.settings')

app = Celery('go_capture')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@app.task
def process_image_task(image_filename):
    sgf_filename = f'{Path(image_filename).stem}.sgf'
    sgf_path = settings.SGF_DIR / sgf_filename
    with open(image_filename, 'rb') as image_file:
        with open(sgf_path, 'w') as sgf_file:
            process_image(image_file, sgf_file)
