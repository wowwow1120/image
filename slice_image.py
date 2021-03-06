import os
import sys
from PIL import Image
import random
from random import shuffle
import numpy as np


def flipping(img):
    # img = Image.open(img_name)
    img = np.array(img)
    img_flip = np.flipud(img)
    return Image.fromarray(img_flip)


def mirroring(img):
    # img = Image.open(img_name)
    img = np.array(img)
    img_mir = np.fliplr(img)
    return Image.fromarray(img_mir)


def rotate(img):
    # img = Image.open
    img = np.array(img)
    img_rot = np.rot90(img)
    return Image.fromarray(img_rot)


def random_transform(img):
    if bool(random.getrandbits(1)):
        img = flipping(img)
    if bool(random.getrandbits(1)):
        img = mirroring(img)
    if bool(random.getrandbits(1)):
        img = rotate(img)
    return img


def image_crop(infilename, col_num, row_num, out_path):
    img = Image.open(infilename)
    (img_h, img_w) = img.size
    print(img.size)

    col_num = int(col_num)
    row_num = int(row_num)
    col_extra = img_w % col_num
    row_extra = img_h % row_num

    if col_extra == 0:
        grid_w = img_w / col_num  # crop width(int)
    else:
        grid_w = (img_w - col_extra) / col_num  # crop width(not_int)

    if row_extra == 0:
        grid_h = img_h / row_num  # crop height(int)
    else:
        grid_h = (img_h - row_extra) / row_num  # crop height(not_int)
    print(grid_w, grid_h)

    img_num = list(range(1, col_num * row_num + 1))

    shuffle(img_num)
    print(img_num)
    i = 0
    for w in range(col_num):
        for h in range(row_num):
            img_box = (h * grid_h, w * grid_w, (h + 1) * grid_h, (w + 1) * grid_w)
            print(h * grid_h, w * grid_w, (h + 1) * grid_h, (w + 1) * grid_w)
            crop_img = img.crop(img_box)
            transformed_img = random_transform(crop_img)
            fname = '0' + str(img_num[i]) if img_num[i] / 10 < 1 else str(img_num[i])
            full_name = fname + '.jpg'
            savename = os.path.join(out_path, full_name)
            transformed_img.save(savename)
            print('save file ' + savename + '....')
            i += 1




if __name__ == '__main__':
    image_file_name = sys.argv[1]
    column_number = sys.argv[2]
    row_number = sys.argv[3]
    prefix_output_filename = sys.argv[4]
    image_crop(image_file_name , column_number , row_number, prefix_output_filename)