from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def capture(request):
    image_file = request.FILES['image']
    default_storage.save(image_file.name, image_file)
    return HttpResponse(status=201)
