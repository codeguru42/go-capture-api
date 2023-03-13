from pathlib import Path

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET

from go_capture.tasks import process_image_task


@require_POST
def capture(request):
    image_file = request.FILES['image']
    filename = Path(image_file.name)
    output_path = settings.IMAGES_DIR / filename
    with output_path.open('wb') as output_file:
        output_file.write(image_file.read())
    process_image_task.delay(str(output_path.absolute()))
    return HttpResponse(status=201)


@require_GET
def health_check(request):
    body = {
        'message': 'Healthy!'
    }
    return JsonResponse(body)
