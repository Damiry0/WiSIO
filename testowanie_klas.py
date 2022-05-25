


import cv2 as cv
import numpy as np
import os
from PIL import Image
from itertools import product


class Fragment:
    def __init__(self, tilefname, offset):
        self.tilefname = tilefname
        self.offset = offset


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each photo in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('boards')  # changing current directory to 'boards'

# checking if there is an output folder to stash the tiles in, if not, creating one
if not os.path.isdir('output'):
    os.mkdir('output')


def tile(filename, dir_out, tile_list, div_w=10, div_h=10):
    """
    @param filename: name of the photo that needs to be divided
    @param dir_out: name of the directory to stash the tiles
    @param tile_list: a list in which names and offset of the tiles will be saved
    @param div_w: divider of image width
    @param div_h: divider of image height
    @return:
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


list_of_frames = []
number_of_photos = tile("dobra_wycieta.png", "output/", list_of_frames)
print(range(number_of_photos))
print(list_of_frames[0].offset)


