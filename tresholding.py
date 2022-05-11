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

number_of_photos=tile("boards/dobra_wycieta.png","output/",256)

for i in range(number_of_photos):

    haystack_img = cv.imread('boards/zla_wycieta.png', 0)
    needle_img = cv.imread(f'output/boards/dobra_wycieta_{i}.png', 0)

    result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)

    # I've inverted the threshold and where comparison to work with TM_SQDIFF_NORMED
    threshold = 0.07
    locations = np.where(result <= threshold)
    # We can zip those up into a list of (x, y) position tuples
    locations = list(zip(*locations[::-1]))
    print(locations)

    if locations:
        print('Found needle.')

        needle_w = needle_img.shape[1]
        needle_h = needle_img.shape[0]
        line_color = (120, 120, 0)
        line_type = cv.LINE_4
        # Loop over all the locations and draw their rectangle
        for loc in locations:
            # Determine the box positions
            top_left = loc
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
            # Draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

        res=cv.resize(haystack_img,(960,540))
        cv.imshow('Matches', res)
        cv.waitKey()

    else:
        print('Needle not found.')