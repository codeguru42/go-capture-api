from django.http import FileResponse
from django.views.decorators.http import require_POST


@require_POST
def capture(request):
    image_file = request.FILES['image']
    return FileResponse(image_file, filename="baord.jpg", status=201, as_attachment=True)
