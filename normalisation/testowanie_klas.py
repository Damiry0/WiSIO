import cv2 as cv
import numpy as np
import os
from PIL import Image
from itertools import product


class Fragment:
    def __init__(self, tilefname, offset):
        self.tilefname = tilefname
        self.offset = offset


# if not os.path.isdir(dir):
#     os.mkdir(dir)

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each photo in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('../boards')  # nie mam pojęcia, jak tobie to działa niby, więc ja robię tak


list_of_frames = []

# d - szerokość
# e - wysokość

def tile(filename, dir_out, div_w=10, div_h=10):
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
        list_of_frames.append(Fragment(out, box))
        k = k + 1
        img.crop(box).save(out)
    return k


number_of_photos = tile("dobra_wycieta.png", "output/")

# print(range(number_of_photos))

