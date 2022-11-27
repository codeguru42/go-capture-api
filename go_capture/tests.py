import unittest
from pathlib import Path

import cv2

from go_capture.sgf import find_stones, make_sgf


class FindStonesTests(unittest.TestCase):
    def test_find_stones(self):
        output_path = Path('expected')
        if not output_path.exists():
            output_path.mkdir()

        input_path = Path('./images/whole_board')
        for input_filename in input_path.glob('*'):
            print(input_filename)
            image = cv2.imread(str(input_filename))
            black, white = find_stones.find_stones(image)
            output_file = output_path / (input_filename.stem + '.sgf')
            with output_file.open('w') as output_file:
                make_sgf.make_sgf(output_file, black, white)
