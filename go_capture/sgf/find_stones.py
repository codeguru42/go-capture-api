import cv2
import numpy as np

NONE = 0
BLACK = 1
WHITE = 2


def categorize(patch):
    gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)
    average = np.average(gray)
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
    black = []
    white = []
    for x in range(19):
        for y in range(19):
            top = max(0, y * dy - radius)
            bottom = min(y * dy + radius, height)
            left = max(0, x * dx - radius)
            right = min(x * dx + radius, width)
            patch = board[top:bottom, left:right]
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