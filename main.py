from PIL import Image, ImageChops

import cv2
import imutils

#METHOD 1

#image1 = Image.open('01.JPG')
#image2 = Image.open('01_open_circuit_01.jpg')

#diff = ImageChops.difference(image1, image2)
#if diff.getbbox():
   #diff.show()



# #Method 2

new = cv2.imread('01_open_circuit_01.jpg')
original = cv2.imread('01.JPG')


original = imutils.resize(original, height=600)
new = imutils.resize(new, height=600)
diff = original.copy()
cv2.absdiff(original, new, diff)


gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

for i in range(0,3):
    dilated = cv2.dilate(gray.copy(), None, iterations=i+1)


(T,thresh) = cv2.threshold(dilated, 10, 255, cv2.THRESH_BINARY)

cnts = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

for c in cnts:
    (x,y,w,h) = cv2.boundingRect(c)
    cv2.rectangle(new,(x,y),(x+w,y+h),(0,255,0),2)

cv2.imwrite('changes.png',new)

#
