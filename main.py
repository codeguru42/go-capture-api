import sys

import cv2


def main(filename):
    image = cv2.imread(filename)
    cv2.imshow('Image', image)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv[1])
