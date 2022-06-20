import os
import sys
from pathlib import Path

import cv2
import numpy as np


def contours(filename):
    gray = cv2.imread(str(filename), cv2.IMREAD_GRAYSCALE)
    blank_image = np.zeros((*gray.shape, 3))
    edges = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
    cv2.imshow(str(filename), blank_image)
    cv2.waitKey()


def main(directory):
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        contours(Path(directory) / filename)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
