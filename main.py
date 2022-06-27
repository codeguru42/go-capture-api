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
    output_root = Path('output')
    input_path = Path(directory)

    for file in input_path.glob('*'):
        print(file)
        contours = find_contours(file)
        output_path = output_root / file.stem
        output_path.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path / ('contours' + file.suffix)), contours)


if __name__ == '__main__':
    main(sys.argv[1])
