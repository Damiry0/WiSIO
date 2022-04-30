# rektyfikacja
# obszary wolno zmienne
# https://github.com/evanlev/image_rectification
# https://scikit-image.org/docs/stable/auto_examples/index.html
# https://learnopencv.com/contour-detection-using-opencv-python-c/
# histogram matching (ale długo trwa i w sumie nam się nie przyda XD)

# KWANTYZACJA to się nazywało
# colorReduce()
#div = 64
#res = img // div * div + div // 2

# usuwanie salt and pepper !!!???
# https://quick-adviser.com/how-do-you-remove-salt-and-pepper-noise-in-image-processing/

# https://emrecankuran.medium.com/a-guide-to-contrast-enhancement-transformation-functions-histogram-sliding-contrast-stretching-34149e5cdeed

import numpy as np
import cv2

img = cv2.imread('boards/1good.jpg', 1)

median = cv2.medianBlur(img, 13)
compare = np.concatenate((img, median), axis=1) #side by side comparison

cv2.imshow('img', compare)
cv2.waitKey(0)
cv2.destroyAllWindows

cv2.imwrite('boards/1res.jpg', compare)
