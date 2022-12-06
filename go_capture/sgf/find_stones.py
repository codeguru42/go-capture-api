import cv2
import numpy as np

NONE = 0
BLACK = 1
WHITE = 2


def categorize(patch, label_black, label_white):
    labels, counts = np.unique(patch, return_counts=True)
    label_max = labels[np.argmax(counts)]
    if label_max == label_black:
        return BLACK
    elif label_max == label_white:
        return WHITE
    return NONE


def find_stones(board):
    labeled_image, label_black, label_white = get_clusters(board)
    height, width, _ = board.shape
    dx = width // 18
    dy = height // 18
    patch_width = dx // 2
    patch_height = dy // 2
    black = []
    white = []
    for x in range(19):
        for y in range(19):
            top = max(0, y * dy - patch_height)
            bottom = min(y * dy + patch_height, height)
            left = max(0, x * dx - patch_width)
            right = min(x * dx + patch_width, width)
            patch = labeled_image[top:bottom, left:right]
            stone = categorize(patch, label_black, label_white)
            if stone == BLACK:
                black.append((x, y))
            elif stone == WHITE:
                white.append((x, y))
    return black, white


def draw_patches(image, coords, color):
    height, width, _ = image.shape
    dx = width // 18
    dy = height // 18
    patch_width = dx // 2
    patch_height = dy // 2
    for x, y in coords:
        top = max(0, y * dy - patch_height)
        bottom = min(y * dy + patch_height, height)
        left = max(0, x * dx - patch_width)
        right = min(x * dx + patch_width, width)
        cv2.rectangle(image, (left, top), (right, bottom), color, 2)


def get_clusters(board):
    gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
    width, height = gray.shape
    pixels = np.float32(gray.reshape((width * height)))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, 5, None, criteria, 10, flags)
    return labels.reshape(gray.shape), np.argmin(palette), np.argmax(palette)
