# Executing tresholding.py:
#
# python tresholding.py USER_PARAM_1 USER_PARAM_2 USER_PARAM_3 USER_PARAM_4 USER_PARAM_5 USER_PARAM_6 USER_PARAM_7
# USER_PARAM_1 - name of the file with good board <type string> - default 'dobra_wycieta.png'
# USER_PARAM_2 - name of the file with input board <type string> - default 'zla_wycieta.png'
# USER_PARAM_3 - depth of the algorithm <type int> - default '3'
# USER_PARAM_4 - detecting threshold for primary layer <type float> - default '0.02'
# USER_PARAM_5 - tolerance level update <type float> - default '0.06'
# USER_PARAM_6 - divider of image width (X axis) <type int> - default '2'
# USER_PARAM_7 - divider of image height (Y axis) <type int> - default '2'
#
# Executing:
# tresholding.py dobra_wycieta.png zla_wycieta.png 3 0.02 0.06 2 2
#
# Program saves output file with faults as 'final_board.png' in boards directory

# import cv2 as cv
from cv2 import imread, imwrite, matchTemplate, TM_SQDIFF_NORMED, IMREAD_COLOR, copyMakeBorder, BORDER_CONSTANT
import os
import shutil
import sys
# import numpy as np
from numpy import where

from PIL import Image
from itertools import product


# Change the working directory to the folder this script is in.
application_path = os.path.dirname(sys.executable)
os.chdir(application_path + '\\boards')

if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}",flush=True)
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>8}: {arg}",flush=True)


# checking if there is an output folder to stash the tiles in, if not, creating one
if not os.path.isdir('output'):
    os.mkdir('output')
else:
    # removing files from output if there is any
    for path in os.scandir('output/'):
        if path.is_file():
            os.remove(path)

if not os.path.isdir('output_temp'):
    os.mkdir('output_temp')

# Class that is used to keep the tile name and its offset
class Fragment:
    def __init__(self, tilefname, offset):
        self.tilefname = tilefname
        self.offset = offset


# Function dividing an image into tiles.
# Tiles are saved in given location as images.
def tile(filename, dir_out, tile_list, div_w=10, div_h=10, offset=(0, 0, 0, 0)):
    """
    @param filename: name of the image that needs to be divided
    @param dir_out: name of the directory to stash the tiles
    @param tile_list: a list in which names and offset of the tiles will be saved
    @param div_w: divider of image width
    @param div_h: divider of image height
    @param offset: absolute offset (from point 0,0) of parent frame: (x_start, y_start, x_end, y_end)
    @return: number of tiles
    """
    name, ext = os.path.splitext(filename)
    # z tym trzeba popatrzeć czy to ma sens, czy tu ma być '//', '\\', czy pojedyncze czy co
    name = name.split("\\")[-1]
    img = Image.open(filename)
    w, h = img.size
    w_tile = int(w/div_w)
    h_tile = int(h/div_h)
    k = 0
    print("Pixel loss: h, h_tile, h % h_tile", h, h_tile, h % h_tile,flush=True)
    print("Pixel loss: w, w_tile, w % w_tile", w, w_tile, w % w_tile,flush=True)

    grid = product(range(0, h - h % h_tile, h_tile), range(0, w - w % w_tile, w_tile))
    for i, j in grid:
        box = (j, i, j + w_tile, i + h_tile)
        out = os.path.join(dir_out, f'{name}_{k}{ext}')
        n_offset = [offset[0], offset[1], offset[0], offset[1]]
        add_offset = [sum(x) for x in zip(box, n_offset)]  # adding box and offset elementwise
        tile_list.append(Fragment(out, add_offset))
        k = k + 1
        img.crop(box).save(out)
    return k


def check_adjacent(w_tile, h_tile, x_offset_1, x_offset_2, y_offset_1, y_offset_2):
    """
    :param w_tile: width of a single tile
    :param h_tile: height of a single tile
    :param x_offset_1: offset on the X AXIS from the top left corner of the board of the primary tile
    :param x_offset_2: offset on the X AXIS from the top left corner of the board of the compared tile
    :param y_offset_1: offset on the Y AXIS from the top left corner of the board of the primary tile
    :param y_offset_2: offset on the Y AXIS from the top left corner of the board of the compared tile
    :return: a list of neighbour tile flags
    """
    flag_adjacent = []
    if abs(x_offset_1 - x_offset_2) / w_tile == 1.0 and y_offset_1 == y_offset_2:
        flag_adjacent.append('1')
        if x_offset_1 < x_offset_2:
            flag_adjacent.append('R')
        else:
            flag_adjacent.append('L')
    else:
        flag_adjacent.append('0')

    if abs(y_offset_1 - y_offset_2) / h_tile == 1.0 and x_offset_1 == x_offset_2:
        flag_adjacent.append('1')
        if y_offset_1 < y_offset_2:
            flag_adjacent.append('B')
        else:
            flag_adjacent.append('T')
    else:
        flag_adjacent.append('0')

    return flag_adjacent


def needle_in_hay_stack(haystack_name, number_of_photos, list_of_tiles, threshold=0.07):
    """
    @param haystack_name: name of the ideal board file
    @param number_of_photos: number of tiles, that the ideal board has been broken into
    @param list_of_tiles: the list of tiles information
    @param threshold: the lower the threshold, the more accurate detecting
    @return: None
    """
    list_of_bundles = list_of_tiles.copy()
    for i in range(number_of_photos):
        haystack_img = imread(haystack_name, 0)
        needle_img = imread(list_of_bundles[i].tilefname, 0)

        result = matchTemplate(haystack_img, needle_img, TM_SQDIFF_NORMED)
        # Inverted threshold to work with TM_SQDIFF_NORMED
        locations = where(result <= threshold)
        list2 = [None] * len(locations[0])
        # Writing necessary data to a separate list
        for n in range(len(locations[0])):
            list2[n] = result[locations[0][n]][locations[1][n]]
        # Zipping up into a list of (x, y) position tuples
        locations = list(zip(*locations[::1]))
        list1 = [None] * len(locations)
        # Zipping a new list for later iteration in loop
        locations1 = where(result <= threshold)
        locations1 = list(zip(*locations1[::-1]))

        if locations1:
            print('Found needle.',flush=True)
            list_of_tiles.remove(list_of_bundles[i])
        else:
            print('Needle not found.',flush=True)


# list of errors to display
list_of_frames = []
# list of error subframes
deep_list_of_frames = []
# good image entered by user
source_image = sys.argv[1]     # USER PARAM
# bad image entered by user
input_image = sys.argv[2]     # USER PARAM


'''Dividing into tiles'''
number_of_tiles = tile(source_image, os.getcwd() + r'\output\\', list_of_frames, div_w=2, div_h=2)
print(range(number_of_tiles),flush=True)
# list of images to delete
list_of_all_frames = list_of_frames.copy()

'''Searching for every element from "output" in input frame'''
# print('Dlugosc przed:', len(list_of_frames))
needle_in_hay_stack(input_image, number_of_tiles, list_of_frames, threshold=0.02)
# print('Dlugosc po', len(list_of_frames))

# All frames - not_needle frames = list of needle frames that should be erased from "output"
# Example: We divided source image into 100 tiles. In input image we found 90 of them, and the rest we did not find.
# We don't need the ones we found, so we delete them, and analyse only the remaining 10.
list_to_erase = [not_needle for not_needle in list_of_all_frames if not_needle not in list_of_frames]

# deleting found frames
for item in list_to_erase:
    os.remove(item.tilefname)

# Deep loop for better accuracy?
howDeep = int(sys.argv[3])     # USER PARAM
# starting threshold for first layer
thr = float(sys.argv[4])     # USER PARAM
# threshold raise per loop
thr_grow = float(sys.argv[5])      # USER PARAM

for i in range(howDeep):
    # CHECKING ERROR IMAGES IN OUTPUT
    for frame in list_of_frames:
        number_of_tiles = tile(frame.tilefname, os.getcwd() + r"\output_temp", deep_list_of_frames,
                               int(sys.argv[6]), int(sys.argv[7]), offset=frame.offset)
        list_of_all_frames = deep_list_of_frames.copy()
        needle_in_hay_stack(input_image, number_of_tiles, deep_list_of_frames, threshold=thr)
        list_to_erase = [not_needle for not_needle in list_of_all_frames if not_needle not in deep_list_of_frames]

        for item in list_to_erase:
            os.remove(item.tilefname)

    # PUTTING subFRAMES INTO OUTPUT AND CHANGING list_of_frames - now subframes become frames
    # removing files from output
    for path in os.scandir('output/'):
        if path.is_file():
            os.remove(path)
    # transferring files from output_temp to output
    for path in os.scandir('output_temp/'):
        if path.is_file():
            shutil.move(path, os.getcwd()+r'\output')

    # changing list of frames
    for item in deep_list_of_frames:
        item.tilefname = 'output\\' + item.tilefname.split('\\')[-1]
        print(item.tilefname,flush=True)

    list_of_frames = deep_list_of_frames.copy()
    deep_list_of_frames = []
    thr += thr_grow

Image1 = Image.open(source_image)
Image1copy = Image1.copy()

w_tile = abs(list_of_frames[0].offset[0] - list_of_frames[0].offset[2])
h_tile = abs(list_of_frames[0].offset[1] - list_of_frames[0].offset[3])

print("Tile width", w_tile,flush=True)
print("Tile height", h_tile,flush=True)
value = [240, 38, 38]

border_hor_size = int((2*5*Image1.size[0]*Image1.size[1])/4410944)
border_ver_size = border_hor_size
grid_size = int((2*1*Image1.size[0]*Image1.size[1])/4410944)


for square in list_of_frames:
    pos = []
    for item in list_of_frames:
        flag = check_adjacent(w_tile, h_tile, square.offset[0], item.offset[0], square.offset[1], item.offset[1])
        if flag[0] != '0':
            pos.append(flag[1])
            if flag[2]!='0':
                pos.append(flag[3])
        elif flag[0] == '0' and flag[1] !='0':
            pos.append(flag[2])
    # size (width of line) of the fault tile border
    border_right = border_ver_size
    border_left = border_ver_size
    border_top = border_hor_size
    border_bottom = border_hor_size
    if 'R' in pos:
         border_right = grid_size
    if 'L' in pos:
         border_left = grid_size
    if 'T' in pos:
         border_top = grid_size
    if 'B' in pos:
         border_bottom = grid_size

    src = imread(square.tilefname, IMREAD_COLOR)
    dst = copyMakeBorder(src, border_top, border_bottom, border_left, border_right, BORDER_CONSTANT, None, value)
    imwrite(square.tilefname, dst)
    temp_img = Image.open(square.tilefname)

    Image1copy.paste(temp_img, (square.offset[0] - border_left, square.offset[1] - border_top))

Image1copy.save("final_board.png")


