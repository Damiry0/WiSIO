# to mamy 6 metod template matchingu do wykrywania elementu template na podanym zdjęciu img.
# nie wiem, czy zwykłe szukanie różnic wypali, więc możnaby:
# - podzielić obrazek wzorcowy na prostokąty i w obrazku wejściowym szukać prostokątów ze wzorca
# - jeśli template został znaleziony w danym miejscu, to zamalowujemy ten obszar na czarno
# - kiedy sprawdziliśmy wszystkie prostokąty, to teoretycznie wszystkie "nieczarne" obszary powinny być obszarami,
# na których są różnice


import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread('boards/3defects.jpg',0)
img2 = img.copy()
template = cv.imread('boards/part.jpg',0)
w, h = template.shape[::-1]
# All the 6 methods for comparison in a list
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv.rectangle(img,top_left, bottom_right, 255, -1)
    plt.subplot(121),plt.imshow(res,cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()