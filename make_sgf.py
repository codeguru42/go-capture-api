import sys

import cv2
import numpy as np

import perspective

NONE = 0
BLACK = 1
WHITE = 2


def categorize(patch):
    average = np.average(patch)
    if average < 60:
        return BLACK
    elif average > 180:
        return WHITE
    return NONE


def find_stones(board):
    height, width, _ = board.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    black = []
    white = []
    for x in range(19):
        for y in range(19):
            top = max(0, y * dy - radius)
            bottom = min(y * dy + radius, height)
            left = max(0, x * dx - radius)
            right = min(x * dx + radius, width)
            patch = gray[top:bottom, left:right]
            stone = categorize(patch)
            if stone == BLACK:
                black.append((x, y))
            elif stone == WHITE:
                white.append((x, y))
    return black, white


def draw_patches(image, coords, color):
    height, width, _ = image.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4
    for x, y in coords:
        top = max(0, y * dy - radius)
        bottom = min(y * dy + radius, height)
        left = max(0, x * dx - radius)
        right = min(x * dx + radius, width)
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)


def main(filename):
    try:
        image = cv2.imread(filename)
        transformed = perspective.get_grid(image)

        cv2.imshow('transformed', transformed)
        cv2.waitKey()

        black, white = find_stones(transformed)

        draw_patches(transformed, black, (255, 0, 0))
        draw_patches(transformed, white, (0, 255, 0))

        cv2.imshow('transformed', transformed)
        cv2.waitKey()
        cv2.imwrite('board2.png', transformed)
    finally:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
