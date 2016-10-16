import os
import numpy as np
from PIL import Image

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "resources", "image")


def format_image_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_IMAGE_RESOURCES, path)
        return new_path
    return path

def image_to_bin(path):
    img = Image.open(format_image_path(path)).convert('L')
    img_arr = np.array(img)
    bin_arr = []
    for row in img_arr:
        row_arr = []
        for pixel in row:
            row_arr.append('{:08b}'.format(pixel))
        bin_arr.append(row_arr)
    return bin_arr

def bin_to_image(bin_arr, path):
    img_arr = []
    for row in bin_arr:
        row_arr = []
        for pixel in row:
            row_arr.append(int(pixel, 2))
        img_arr.append(row_arr)
    img_arr = np.array(img_arr, dtype=np.int8)

    img = Image.fromarray(img_arr, mode="L")
    img.save(format_image_path(path), 'PNG')


# Especificaciones del Codigo Hamming (12,8):
# Información: 8 bits
# Paridad: 4 bits
