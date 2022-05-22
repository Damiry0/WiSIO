import cv2 as cv
import numpy as np
import os
from PIL import Image
from itertools import product


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))




def tile(filename, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w, h = img.size
    k=0
    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    for i, j in grid:
        box = (j, i, j + d, i + d)
        out = os.path.join(dir_out, f'{name}_{k}{ext}')
        k = k + 1
        img.crop(box).save(out)
    return k

number_of_photos=tile("dobra_wycieta.png","output/",256)
print(range(number_of_photos))

for i in range(number_of_photos):
    haystack_img = cv.imread('zla_wycieta.png', 0)
    needle_img = cv.imread(f'output/dobra_wycieta_{i}.png', 0)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)

    # I've inverted the threshold and where comparison to work with TM_SQDIFF_NORMED
    threshold = 0.07
    locations = np.where(result <= threshold)
    list2  = [None] * len(locations[0])
    # Writing nescessary data to a seperate list
    for i in range(len(locations[0])):
        list2[i] = result[locations[0][i]][locations[1][i]]

    # We can zip those up into a list of (x, y) position tuples
    locations = list(zip(*locations[::1]))
    list1  = [None] * len(locations)
    # Zipping a new list for later iteration in loop
    locations1 = np.where(result <= threshold)
    locations1 = list(zip(*locations1[::-1]))

    if locations1:
        # Getting index of most similar image
        location_index = list2.index(min(list2))
        location = locations1[location_index]
        print('Found needle.')

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]
        line_color = (120, 120, 0)
        line_type = cv.LINE_4
        # Drawing a rectangle
        # Determine the box positions
        top_left = location
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        res=cv.resize(haystack_img,(960,540))
        cv.imshow('Matches', res)
        cv.waitKey()

    else:
        print('Needle not found.')





