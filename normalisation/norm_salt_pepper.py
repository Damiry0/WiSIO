import numpy as np
import cv2

img = cv2.imread('../boards/1good.jpg', 1)

median = cv2.medianBlur(img, 13)
compare = np.concatenate((img, median), axis=1) #side by side comparison

cv2.imshow('img', compare)
cv2.waitKey(0)
cv2.destroyAllWindows

cv2.imwrite('../boards/1res.jpg', compare)