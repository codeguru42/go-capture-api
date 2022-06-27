import os
import sys
from pathlib import Path

import cv2
import numpy as np


def find_contours(filename):
    gray = cv2.imread(str(filename), cv2.IMREAD_GRAYSCALE)
    blank_image = np.zeros((*gray.shape, 3))
    edges = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
    return blank_image


def main(directory):
    if not os.path.exists('output'):
        os.mkdir('output')
    for file in os.listdir(directory):
        print(file)
        filename = os.fsdecode(file)
        contours = find_contours(Path(directory) / filename)
        cv2.imwrite(str(Path('output') / filename), contours)


if __name__ == '__main__':
    main(sys.argv[1])
