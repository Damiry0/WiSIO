# This programs calculates the orientation of an object.
# The input is an image, and the output is an annotated image
# with the angle of otientation for each object (0 to 180 degrees)

import cv2 as cv
from math import atan2, cos, sin, sqrt, pi
import numpy as np

# Load the image
img = cv.imread("../boards/1good.jpg")

# Was the image there?
if img is None:
    print("Error: File not found")
    exit(0)

#cv.imshow('Input Image', img)

# Convert image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Convert image to binary
_, bw = cv.threshold(gray, 50, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

# Find all the contours in the thresholded image
contours, _ = cv.findContours(bw, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

# height of image in pixels
height = img.shape[0]
width = img.shape[1]

for i, c in enumerate(contours):

    # Calculate the area of each contour
    area = cv.contourArea(c)

    # Ignore contours that are too small or too large
    if area < (width*height)/2 or area >= (width*height):
        continue

    # cv.minAreaRect returns:
    # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
    rect = cv.minAreaRect(c)
    box = cv.boxPoints(rect)
    box = np.int0(box)

    # Retrieve the key parameters of the rotated bounding box
    center = (int(rect[0][0]), int(rect[0][1]))
    width = int(rect[1][0])
    height = int(rect[1][1])
    angle = int(rect[2])

    if width < height:
        angle = 90 - angle
    else:
        angle = -angle

    label = "  Rotation Angle: " + str(angle) + " degrees"
    textbox = cv.rectangle(img, (center[0] - 35, center[1] - 25),
                           (center[0] + 295, center[1] + 10), (255, 255, 255), -1)
    cv.putText(img, label, (center[0] - 50, center[1]),
               cv.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 3, cv.LINE_AA)
    cv.drawContours(img, [box], 0, (0, 0, 255), 2)

#cv.imshow('Output Image', img)
cv.waitKey(0)
cv.destroyAllWindows()

# Save the output image to the current directory
cv.imwrite("../boards/area_rec.jpg", img)