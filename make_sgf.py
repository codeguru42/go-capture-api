import sys

import cv2
import numpy as np

import perspective


def main(filename):
    image = cv2.imread(filename)
    transformed = perspective.get_grid(image)
    width, height, _ = transformed.shape
    dx = width // 18
    dy = height // 18
    radius = dx // 4

    gray = cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY)

    for x in range(19):
        for y in range(19):
            average = np.average(gray[y*dy-radius:y*dy+radius,x*dx-radius:x*dx+radius])
            if average < 50:
                color = (255, 0, 0)
            elif average > 200:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            cv2.circle(transformed, (x * dx, y * dy), radius, color, cv2.FILLED)

    cv2.imshow('transformed', transformed)
    cv2.waitKey()
    cv2.imwrite('board.png', transformed)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
