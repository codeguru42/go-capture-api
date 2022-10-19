import sys

import cv2
import numpy as np

import perspective

NONE = 0
BLACK = 1
WHITE = 2


def categorize(patch):
    width, height = patch.shape
    pixels = np.float32(patch.reshape((width*height)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, 3, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)
    dominant = palette[np.argmax(counts)]
    if dominant[0] < 50:
        return BLACK
    elif dominant[0] > 200:
        return WHITE
    return NONE


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
            top = y * dy - radius
            bottom = y * dy + radius
            left = x * dx - radius
            right = x * dx + radius
            patch = gray[max(0, top):min(bottom, height), max(0, left):min(right, width)]
            stone = categorize(patch)
            if stone == BLACK:
                black.append((x, y))
            elif stone == WHITE:
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
