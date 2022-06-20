import sys

import cv2


def main(filename):
    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 200)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
