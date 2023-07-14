import io
from pathlib import Path

import cv2
import pytest

from sgf import find_stones, make_sgf, perspective


def get_images(image_folder):
    image_path = Path(image_folder)
    for image_filename in image_path.glob("*.jpg"):
        yield image_filename


@pytest.mark.parametrize(
    "image_filename", list(get_images("../images/whole_board")), ids=lambda x: x.stem
)
def test_whole_board(image_filename):
    image = cv2.imread(str(image_filename))
    board = perspective.get_grid(image)
    black, white = find_stones.find_stones(board)
    out_stream = io.StringIO()
    make_sgf.make_sgf(out_stream, black, white)
    expected_path = Path("../expected") / (image_filename.stem + ".sgf")
    with expected_path.open() as expected_file:
        expected = expected_file.readlines()
    out_stream.seek(0)
    assert out_stream.read() == "".join(expected)
