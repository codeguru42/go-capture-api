import io
from pathlib import Path

from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET

from go_capture.sgf.process_image import process_image


@require_POST
def capture(request):
    image_file = request.FILES['image']
    output_file = io.StringIO()
    process_image(image_file, output_file)
    output_file.seek(0)
    filename = Path(image_file.name).stem
    return FileResponse(
        output_file.read(),
        status=201,
        filename=f'${filename}.sgf',
        as_attachment=True,
        content_type='application/x-go-sgf'
    )


@require_GET
def health_check(request):
    body = {
        'message': 'Healthy!'
    }
    return JsonResponse(body)
