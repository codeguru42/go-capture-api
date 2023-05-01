import cv2
import numpy as np


def dist(x1, x2, y1, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def perspective_transform(image, corners):
    # Order points in clockwise order
    top_r, top_l, bottom_l, bottom_r = np.reshape(corners, (4, 2))

    # Determine width of new image which is the max distance between
    # (bottom right and bottom left) or (top right and top left) x-coordinates
    width_bottom = dist(bottom_r[0], bottom_l[0], bottom_r[1], bottom_l[1])
    width_top = dist(top_r[0], top_l[0], top_r[1], top_l[1])
    width = max(int(width_bottom), int(width_top))

    # Determine height of new image which is the max distance between
    # (top right and bottom right) or (top left and bottom left) y-coordinates
    height_right = dist(top_r[0], bottom_r[0], top_r[1], bottom_r[1])
    height_left = dist(top_l[0], bottom_l[0], top_l[1], bottom_l[1])
    height = max(int(height_right), int(height_left))

    # Construct new points to obtain top-down view of image in
    # top_r, top_l, bottom_l, bottom_r order
    dimensions = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype="float32",
    )

    # Convert to Numpy format
    ordered_corners = np.array((top_l, top_r, bottom_r, bottom_l), dtype="float32")

    # Find perspective transform matrix
    matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)

    # Return the transformed image
    return cv2.warpPerspective(image, matrix, (width, height))


def get_corners(image):
    copy = image.copy()
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 3)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3
    )
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return sorted_contours[0]


def get_grid(image):
    corners = get_corners(image)
    peri = cv2.arcLength(corners, True)
    approx = cv2.approxPolyDP(corners, 0.015 * peri, True)
    transformed = perspective_transform(image, approx)
    return transformed
