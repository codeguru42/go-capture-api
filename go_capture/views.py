import cv2
import numpy as np
from django.http import FileResponse
from django.views.decorators.http import require_POST

from go_capture.sgf import perspective, find_stones


@require_POST
def capture(request):
    image_file = request.FILES['image']
    image_data = np.asarray(bytearray(image_file.read()), dtype="uint8")
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    board = perspective.get_grid(image)
    black, white = find_stones.find_stones(board)
    find_stones.draw_patches(board, black, (0, 0, 255))
    find_stones.draw_patches(board, white, (0, 0, 255))
    return FileResponse(board, filename="board.jpg", status=201, as_attachment=True)
