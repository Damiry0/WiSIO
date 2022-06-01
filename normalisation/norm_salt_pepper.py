import numpy as np
import cv2

distortion = 1

img = cv2.imread('../boards/zla_wycieta.png', 1)

median = cv2.medianBlur(img, distortion)
# compare = np.concatenate((img, median), axis=1) #side by side comparison

# cv2.imshow('img', median)
# cv2.destroyAllWindows

cv2.imwrite('../boards/zla_bez_soli.png', median)


img = cv2.imread('../boards/dobra_wycieta.png', 1)

median = cv2.medianBlur(img, distortion)
# compare = np.concatenate((img, median), axis=1) #side by side comparison

# cv2.imshow('img', compare)
# cv2.destroyAllWindows

cv2.imwrite('../boards/dobra_bez_soli.png', median)