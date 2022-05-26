import cv2 as cv
import numpy as np
import os
from PIL import Image
from itertools import product


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('boards')

# checking if there is an output folder to stash the tiles in, if not, creating one
if not os.path.isdir('output'):
    os.mkdir('output')


# Class that is used to keep the tile name and it's offset
class Fragment:
    def __init__(self, tilefname, offset):
        self.tilefname = tilefname
        self.offset = offset


# Function dividing an image into tiles.
# Tiles are saved in given location as images.
def tile(filename, dir_out, tile_list, div_w=10, div_h=10):
    """
    @param filename: name of the photo that needs to be divided
    @param dir_out: name of the directory to stash the tiles
    @param tile_list: a list in which names and offset of the tiles will be saved
    @param div_w: divider of image width
    @param div_h: divider of image height
    @return: number of tiles
    """
    name, ext = os.path.splitext(filename)
    img = Image.open(filename)
    w, h = img.size
    w_tile = int(w/div_w)
    h_tile = int(h/div_h)
    k = 0
    grid = product(range(0, h - h % h_tile, h_tile), range(0, w - w % w_tile, w_tile))
    for i, j in grid:
        box = (j, i, j + w_tile, i + h_tile)
        out = os.path.join(dir_out, f'{name}_{k}{ext}')
        tile_list.append(Fragment(out, box))
        k = k + 1
        img.crop(box).save(out)
    return k

# it's gonna end up as a list of errors
list_of_frames = []

number_of_tiles = tile("dobra_wycieta.png", "output/", list_of_frames)
print(range(number_of_tiles))
# it's gonna be a list of images to delete
list_of_all_frames = list_of_frames.copy()
print("czy udało sięskopiowąc?", len(list_of_all_frames))



def needle_in_hay_stack(haystack_name, number_of_photos, list_of_tiles):
    """
    @param haystack_name: name of the ideal board file
    @param number_of_photos: number of tiles, that the ideal board has been broken into
    @param list_of_tiles: the list of tiles information
    @return: None
    """
    list_of_bundles = list_of_tiles.copy()
    for i in range(number_of_photos):
        haystack_img = cv.imread(haystack_name, 0)
        needle_img = cv.imread(list_of_bundles[i].tilefname, 0)

        result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)

        # I've inverted the threshold and ???where??? comparison to work with TM_SQDIFF_NORMED
        threshold = 0.07
        locations = np.where(result <= threshold)
        list2 = [None] * len(locations[0])
        # Writing necessary data to a separate list
        for n in range(len(locations[0])):
            list2[n] = result[locations[0][n]][locations[1][n]]
        # We can zip those up into a list of (x, y) position tuples
        locations = list(zip(*locations[::1]))
        list1 = [None] * len(locations)
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
            res = cv.resize(haystack_img, (960, 540))
            #cv.imshow('Matches', res)
            #cv.waitKey()
            list_of_tiles.remove(list_of_bundles[i])
        else:
            print('Needle not found.')


print('Dlugosc przed:', len(list_of_frames))
needle_in_hay_stack('zla_wycieta.png', number_of_tiles, list_of_frames)
print('Dlugosc po', len(list_of_frames))


new_list = [fruit for fruit in list_of_all_frames if fruit not in list_of_frames]
print('Dlugosc listy do usuniecia', len(new_list))

for item in new_list:
    os.remove(item.tilefname)




