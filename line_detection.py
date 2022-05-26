import cv2 as cv
import numpy as np
import math
import os

os.chdir('boards')


src_img = cv.imread('krawedz.png')
cv.imshow('Original Image', src_img)
cv.waitKey(0)

# TUUUU w miejsce tego wstawić tego sobela i gragient magnitude i obraz wynikowy dać do lines
# dst_img = cv.Canny(src_img, 50, 200, None, 3)

cv.imshow('Dist Image', dst_img)
cv.waitKey(0)
lines = cv.HoughLines(dst_img, 1, np.pi / 180, 150, None, 0, 0)

for i in range(0, len(lines)):
            rho_l = lines[i][0][0]
            theta_l = lines[i][0][1]
            a_l = math.cos(theta_l)
            b_l = math.sin(theta_l)
            x0_l = a_l * rho_l
            y0_l = b_l * rho_l
            pt1_l = (int(x0_l + 1000*(-b_l)), int(y0_l + 1000*(a_l)))
            pt2_l = (int(x0_l - 1000*(-b_l)), int(y0_l - 1000*(a_l)))
            cv.line(src_img, pt1_l, pt2_l, (0,0,255), 3, cv.LINE_AA)

cv.imshow("Image with lines", src_img)
cv.waitKey(0)
