import io
from pathlib import Path

import cv2

from go_capture.sgf import find_stones, make_sgf, perspective


def test_whole_board():
    input_path = Path('../images/whole_board')
    for input_filename in input_path.glob('*'):
        print(input_filename)
        image = cv2.imread(str(input_filename))
        board = perspective.get_grid(image)
        black, white = find_stones.find_stones(board)
        out_stream = io.StringIO()
        make_sgf.make_sgf(out_stream, black, white)
        expected_path = Path('../expected') / (input_filename.stem + '.sgf')
        with expected_path.open() as expected_file:
            expected = expected_file.readlines()
        out_stream.seek(0)
        assert ''.join(expected) == out_stream.read()
