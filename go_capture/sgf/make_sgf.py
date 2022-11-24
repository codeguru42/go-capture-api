import os.path
import sys

import cv2

from . import find_stones
from . import perspective


def write_stones(file, stones):
    for x, y in stones:
        file.write(f'[{chr(x + ord("a"))}{chr(y + ord("a"))}]')


def make_sgf(filename, black, white):
    with open(filename, 'w') as file:
        file.write('(;FF[4]\n')
        file.write('GM[1]\n')
        file.write(';AB')
        write_stones(file, black)
        file.write('\n;AW')
        write_stones(file, white)
        file.write('\n)')


def main(image_path):
    image = cv2.imread(image_path)
    board = perspective.get_grid(image)
    black, white = find_stones.find_stones(board)
    filename, _ = os.path.splitext(image_path)
    make_sgf(filename + '.sgf', black, white)


if __name__ == '__main__':
    main(sys.argv[1])
