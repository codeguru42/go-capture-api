import io
from pathlib import Path

from django.conf import settings
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_POST, require_GET

from go_capture.sgf.process_image import process_image
from go_capture.tasks import process_image_task


@require_POST
def capture(request):
    image_file = request.FILES["image"]
    output_file = io.StringIO()
    process_image(image_file, output_file)
    output_file.seek(0)
    filename = Path(image_file.name).stem
    return FileResponse(
        output_file.read(),
        status=201,
        filename=f"${filename}.sgf",
        as_attachment=True,
        content_type="application/x-go-sgf",
    )


@require_POST
def capture_async(request):
    image_file = request.FILES["image"]
    fcm_token = request.POST["fcm_registration_token"]
    print(f"token: {fcm_token}")
    filename = Path(image_file.name)
    print(filename)
    output_path = settings.IMAGES_DIR / filename
    with output_path.open("wb") as output_file:
        output_file.write(image_file.read())
    process_image_task.delay(str(output_path.absolute()), fcm_token)
    return HttpResponse(status=201)


@require_GET
def health_check(request):
    body = {"message": "Healthy!"}
    return JsonResponse(body)
