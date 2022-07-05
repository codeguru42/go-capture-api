import shutil
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


def find_corners(filename):
    img = cv2.imread(str(filename))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)
    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01 * dst.max()] = [0, 255, 0]
    return img


def main(directory):
    output_root = Path('output')
    input_path = Path(directory)

    for file in input_path.glob('*'):
        print(file)
        contours = find_contours(file)
        corners = find_corners(file)
        output_path = output_root / file.stem
        output_path.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file, output_path / ('original' + file.suffix))
        cv2.imwrite(str(output_path / ('contours' + file.suffix)), contours)
        cv2.imwrite(str(output_path / ('corners' + file.suffix)), corners)


if __name__ == '__main__':
    main(sys.argv[1])
