import cv2
import numpy as np

from sgf import perspective, find_stones
from sgf.make_sgf import make_sgf


def process_image(image_file, output_file):
    image_data = np.asarray(bytearray(image_file.read()), dtype="uint8")
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    board = perspective.get_grid(image)
    black, white = find_stones.find_stones(board)
    make_sgf(output_file, black, white)
