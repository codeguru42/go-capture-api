import sys

import cv2

import perspective


def main(filename):
    image = cv2.imread(filename)
    transformed = perspective.get_grid(image)
    width, height, _ = transformed.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4
    for x in range(0, width, dx):
        for y in range(0, height, dy):
            cv2.circle(transformed, (x, y), radius, (0, 255, 0), cv2.FILLED)
    cv2.imshow('transformed', transformed)
    cv2.imwrite('board.png', transformed)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
