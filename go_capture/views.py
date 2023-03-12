import io
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET

from go_capture.sgf.process_image import process_image


@require_POST
def capture(request):
    image_file = request.FILES['image']
    filename = Path(image_file.name)
    output_path = settings.IMAGES_DIR / filename
    with output_path.open('wb') as output_file:
        output_file.write(image_file.read())
    return HttpResponse(status=201)


@require_GET
def health_check(request):
    body = {
        'message': 'Healthy!'
    }
    return JsonResponse(body)
