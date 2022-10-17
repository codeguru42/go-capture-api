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


def find_lines(filename):
    gray = cv2.imread(str(filename), cv2.IMREAD_GRAYSCALE)

    kernel_size = 5
    blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blur, low_threshold, high_threshold)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 50  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    line_image = np.zeros((*gray.shape, 3))
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    return line_image


def main(filename):
    input_file = Path(filename)
    output_root = Path('output')

    print(input_file)
    lines = find_lines(input_file)
    output_path = output_root / input_file.stem
    output_path.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_file, output_path / ('original' + input_file.suffix))
    cv2.imwrite(str(output_path / ('lines' + input_file.suffix)), lines)


if __name__ == '__main__':
    main(sys.argv[1])
