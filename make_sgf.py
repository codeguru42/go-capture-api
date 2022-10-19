import sys

import cv2
import numpy as np

import perspective


def find_stones(board):
    width, height, _ = board.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    black = []
    white = []
    for x in range(19):
        for y in range(19):
            patch = gray[y * dy - radius:y * dy + radius, x * dx - radius:x * dx + radius]
            average = np.average(patch)
            if average < 50:
                black.append((x, y))
            elif average > 200:
                white.append((x, y))
    return black, white


def main(filename):
    image = cv2.imread(filename)
    transformed = perspective.get_grid(image)
    black, white = find_stones(transformed)

    width, height, _ = transformed.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4
    for x, y in black:
        cv2.circle(transformed, (x * dx, y * dy), radius, (255, 0, 0), cv2.FILLED)
    for x, y in white:
        cv2.circle(transformed, (x * dx, y * dy), radius, (0, 255, 0), cv2.FILLED)

    cv2.imshow('transformed', transformed)
    cv2.waitKey()
    cv2.imwrite('board.png', transformed)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
