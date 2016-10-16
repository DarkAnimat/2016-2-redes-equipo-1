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


def bin_to_image(bin_arr):
    img_arr = []
    for row in bin_arr:
        row_arr = []
        for pixel in row:
            row_arr.append(int(pixel, 2))
        img_arr.append(row_arr)
    img_arr = np.array(img_arr, dtype=np.int8)
    img = Image.fromarray(img_arr, mode="L")
    return img

def save_image(image, path):
    image.save(format_image_path(path), 'JPEG')

# Especificaciones del Codigo Hamming (12,8):
M = 8   # Información (M): 8 bits
K = 4   # Paridad (K): 4 bits
        # Para determinarlo: 2^K - 1 >= M + k

def encode_hamming_word(word):

    if (len(word) != M):  raise ValueError('The word length is invalid')

    codeword  = list("x" * (M + K))
    counter = 0

    for i in range(0, len(codeword)):
        if not(is_power2(i+1)):
            codeword[i] = word[counter]
            counter = counter + 1

    for i in range(0, len(codeword)):
        if (is_power2(i+1)):
            codeword[i] = generate_parity_value(i+1, codeword)

    return ''.join(codeword)


def decode_hamming_word(word):
    if (len(word) != (M + K)): raise ValueError('The word length is invalid')

    decoded_word = list("x" * M)

    counter = 0
    for i in range(0, len(word)):
        if not(is_power2(i+1)):
            decoded_word[counter] = word[i]
            counter = counter + 1

    return ''.join(decoded_word)


def is_hamming_word_valid(word):
    if (len(word) != (M + K)): raise ValueError('The word length is invalid')

    valid = True
    for i in range(0, len(word)):
        if (is_power2(i+1)):
            if (word[i] != generate_parity_value(i+1, word)):
                valid = False

    return valid


def generate_parity_value(position, word):
    exponent = obtain_power2_exponent(position)
    ret = ""
    first_found = True
    for i in range(0, len(word)):
        aux = '{:01b}'.format(i+1).zfill(K)
        if(aux[-(exponent+1)] == "1"):
            if (first_found):
                first_found = False
            elif(ret == ""):
                ret = word[i]
            else:
                ret = xor_function(ret, word[i])
    return ret


def is_power2(num):
	return num != 0 and ((num & (num - 1)) == 0)


def obtain_power2_exponent(num):
    if (is_power2(num)):
        counter = 0
        while(num != 1):
            num = num/2
            counter = counter + 1
        return counter
    else:
        return -1


def xor_function(a, b):
    if ((a == "0" and b == "0") or (a == "1" and b == "1")):
        return "0"
    else:
        return "1"
