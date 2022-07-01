from matplotlib.pyplot import hist
from imports import *
from config import *


def escala(img, factor):
    pass

def rot(img, angulo):
    pass

def main():
    img = cv2.imread("img/baboon_perspectiva.png")
    cv2.imshow("Orginal", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()