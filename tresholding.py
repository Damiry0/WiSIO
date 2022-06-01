import cv2 as cv
import numpy as np
import os
from PIL import Image
from itertools import product
import shutil


# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('boards')

# checking if there is an output folder to stash the tiles in, if not, creating one
if not os.path.isdir('output'):
    os.mkdir('output')
else:
    # removing files from output, to make place for
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
    @param filename: name of the photo that needs to be divided
    @param dir_out: name of the directory to stash the tiles
    @param tile_list: a list in which names and offset of the tiles will be saved
    @param div_w: divider of image width
    @param div_h: divider of image height
    @param offset: absolute offset (from point 0,0) of parent frame: (x_start, y_start, x_end, y_end)
    @return: number of tiles
    """
    name, ext = os.path.splitext(filename)
    name = name.split('/')[-1]
    img = Image.open(filename)
    w, h = img.size
    w_tile = int(w/div_w)
    h_tile = int(h/div_h)
    k = 0
    print("strata pikseli: h, h_tile, h % h_tile", h, h_tile, h % h_tile)
    print("strata pikseli w, w_tile, w % w_tile", w, w_tile, w % w_tile)

    grid = product(range(0, h - h % h_tile, h_tile), range(0, w - w % w_tile, w_tile))
    for i, j in grid:
        box = (j, i, j + w_tile, i + h_tile)
        out = os.path.join(dir_out, f'{name}_{k}{ext}')
        add_offset = [sum(x) for x in zip(box, offset)]  # adding box and offset elementwise
        tile_list.append(Fragment(out, add_offset))
        k = k + 1
        img.crop(box).save(out)
    return k


def check_adjacent(w_tile, h_tile, x_offset_1, x_offset_2, y_offset_1, y_offset_2):
    flag_adjacent = []
    if (abs(x_offset_1 - x_offset_2) / w_tile == 1.0 and y_offset_1 == y_offset_2):
        flag_adjacent.append('1')
        if (x_offset_1 < x_offset_2):
            flag_adjacent.append('R')
        else:
            flag_adjacent.append('L')
    else:
        flag_adjacent.append('0')

    if (abs(y_offset_1 - y_offset_2) / h_tile == 1.0 and x_offset_1 == x_offset_2):
        flag_adjacent.append('1')
        if (y_offset_1 < y_offset_2):
            flag_adjacent.append('T')
        else:
            flag_adjacent.append('B')
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
        haystack_img = cv.imread(haystack_name, 0)
        needle_img = cv.imread(list_of_bundles[i].tilefname, 0)

        result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)
        # I've inverted the threshold and ???where??? comparison to work with TM_SQDIFF_NORMED
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


# list of errors to display
list_of_frames = []

deep_list_of_frames = []

'''Dividing into tiles'''
number_of_tiles = tile("dobra_wycieta.png", "output/", list_of_frames, div_w=2, div_h=2)
print(range(number_of_tiles))
# list of images to delete
list_of_all_frames = list_of_frames.copy()

'''Searching for every element from "output" in input frame'''
print('Dlugosc przed:', len(list_of_frames))
needle_in_hay_stack('zla_wycieta.png', number_of_tiles, list_of_frames, threshold=0.02)
print('Dlugosc po', len(list_of_frames))

# All frames - not_needle frames = list of needle frames that should be erased from "output"
# Example: We divided source image into 100 tiles. In input image we found 90 of them, and the rest we did not find.
# We don't need the ones we found, so we delete them, and analyse only the remaining 10.
list_to_erase = [not_needle for not_needle in list_of_all_frames if not_needle not in list_of_frames]
print('Dlugosc listy do usuniecia', len(list_to_erase))

# deleting found frames
for item in list_to_erase:
    os.remove(item.tilefname)

# Deep loop for better accuracy?
howDeep = 2     # USER PARAM
# starting threshold for first layer
thr = 0.02     # USER PARAM
# threshold raise per loop
thr_grow = 0.02     # USER PARAM


for i in range(howDeep):
    # CHECKING ERROR IMAGES IN OUTPUT
    for frame in list_of_frames:
        number_of_tiles = tile(frame.tilefname, "output_temp/", deep_list_of_frames, div_w=2, div_h=2, offset=frame.offset)
        list_of_all_frames = deep_list_of_frames.copy()
        needle_in_hay_stack('zla_wycieta.png', number_of_tiles, deep_list_of_frames, threshold=thr)
        list_to_erase = [not_needle for not_needle in list_of_all_frames if not_needle not in deep_list_of_frames]
        # removing found frames from output_temp/ - tu się wywala przy kolejnym powtórzeniu, bo usuwa płytki z
        # output, zamiast output_temp
        for item in list_to_erase:
            os.remove(item.tilefname)

    # PUTTING subFRAMES INTO OUTPUT AND CHANGING list_of_frames - now subframes become frames

    # removing files from output, to make place for
    for path in os.scandir('output/'):
        if path.is_file():
            os.remove(path)
    # transferring files from output_temp to output
    for path in os.scandir('output_temp/'):
        if path.is_file():
            shutil.move(path, os.getcwd()+r'\output')

    # changing list of frames
    for item in deep_list_of_frames:
        item.tilefname = 'output/' + item.tilefname.split('/')[-1]
        print(item.tilefname)

    # #to niżej nie zadziała chyba tak jak chcę, nie wiem czy nie trzeba będzie uciąć kawałka ścieżki
    list_of_frames = deep_list_of_frames.copy()
    deep_list_of_frames = []
    thr += thr_grow



# Algorytm sprawdzania działa, bo sprawdzałem i dawało dobre rezultaty ale teraz się jebie przez inny tile size
# tile sizy wychodzące poniżej w div_w i div_h są pojebane i kompletnie nie pasują do rzeczywistych tileów
# + jescze nie mam pojęcia czy to wynikowe co wychodzi jest dobre, chyba że zły obraz wziąłem idk
# do omówienia jutro (02.06), a na razie pushuje

Image1 = Image.open("dobra_wycieta.png")
Image1copy = Image1.copy()
w, h = Image1.size
div_w = 2
div_h = 2
w_tile = int(w/div_w)
h_tile = int(h/div_h)
value = [255,255,255]

print("Tile width : ",w_tile)
print("Tile height : ",h_tile)
for square in list_of_frames:
    pos = []
    for item in list_of_frames:
        flag = []
        flag = check_adjacent(w_tile,h_tile,square.offset[0],item.offset[0],square.offset[1],item.offset[1])
        print("Square_offset x : ",square.offset[0])
        print("Square offset y : ",square.offset[1])
        print("item_offset x : ", item.offset[0])
        print("item offset y : ", item.offset[1])
        if flag[0] != '0':
            pos.append(flag[1])
            if(flag[2]!='0'):
                pos.append(flag[3])
        elif (flag[0] == '0' and flag[1] !='0'):
            pos.append(flag[2])
    print("pos flag :",pos)
    border_right = 5
    border_left = 5
    border_top = 5
    border_bottom = 5
    img = Image.open(square.tilefname)
    if 'R' in pos:
        border_right = 0
    if 'L' in pos:
        border_left = 0
    if 'T' in pos:
        border_top = 0
    if 'B' in pos:
        border_top = 0

    src = cv.imread(square.tilefname, cv.IMREAD_COLOR)
    dst = cv.copyMakeBorder(src, border_top, border_bottom, border_left, border_right, cv.BORDER_CONSTANT, None,value)
    cv.imwrite(square.tilefname, dst)
    temp_img = Image.open(square.tilefname)
    Image1copy.paste(temp_img, (square.offset[0] - border_left ,square.offset[1] - border_top))
    Image1copy.save("final_board.png")

Image1copy.show()





