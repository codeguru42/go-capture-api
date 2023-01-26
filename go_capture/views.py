import io

import cv2
import numpy as np
from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET

from go_capture.sgf import perspective, find_stones
from go_capture.sgf.make_sgf import make_sgf


@require_POST
def capture(request):
    image_file = request.FILES['image']
    image_data = np.asarray(bytearray(image_file.read()), dtype="uint8")
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    board = perspective.get_grid(image)
    black, white = find_stones.find_stones(board)
    file = io.StringIO()
    make_sgf(file, black, white)
    file.seek(0)
    return FileResponse(file.read(), status=201, as_attachment=True, content_type='application/x-go-sgf')


@require_GET
def health_check(request):
    body = {
        'message': 'Healthy!'
    }
    return JsonResponse(body)
