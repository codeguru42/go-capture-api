import cv2
import numpy as np

NONE = 0
BLACK = 1
WHITE = 2


def categorize(patch, cutoff_black, cutoff_white):
    average = np.average(patch)
    if average < cutoff_black:
        return BLACK
    elif average > cutoff_white:
        return WHITE
    return NONE


def find_stones(board):
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    cutoff_black, cutoff_white = get_cutoffs(gray)
    height, width, _ = board.shape
    dx = width // 18
    dy = height // 18
    patch_width = dx // 4
    patch_height = dy // 4
    black = []
    white = []
    for x in range(19):
        for y in range(19):
            top = max(0, y * dy - patch_height)
            bottom = min(y * dy + patch_height, height)
            left = max(0, x * dx - patch_width)
            right = min(x * dx + patch_width, width)
            patch = gray[top:bottom, left:right]
            stone = categorize(patch, cutoff_black, cutoff_white)
            if stone == BLACK:
                black.append((x, y))
            elif stone == WHITE:
                white.append((x, y))
    return black, white


def draw_patches(image, coords, color):
    height, width, _ = image.shape
    dx = width // 18
    dy = height // 18
    patch_width = dx // 4
    patch_height = dy // 4
    for x, y in coords:
        top = max(0, y * dy - patch_height)
        bottom = min(y * dy + patch_height, height)
        left = max(0, x * dx - patch_width)
        right = min(x * dx + patch_width, width)
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)


def get_cutoffs(image):
    width, height = image.shape
    pixels = np.float32(image.reshape((width*height)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, 3, None, criteria, 10, flags)
    return np.min(palette), np.max(palette)
