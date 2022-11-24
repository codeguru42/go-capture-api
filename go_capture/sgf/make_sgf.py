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
