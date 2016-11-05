import os
import numpy as np
import math

from PIL import Image

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "resources", "image")

# Encoding info:
STREAM_INFORMATION_BITS_QTY = 256  # Quantity of bits used for storing information on a data-stream
STREAM_PARITY_BITS_QTY = 9         # Quantity of bits used for parity values on a data-stream
STREAM_LENGTH = STREAM_INFORMATION_BITS_QTY + STREAM_PARITY_BITS_QTY # Quantity of bits on a data-stream

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
    return np.array(bin_arr)

def encode_bin_arr(bin_arr):

    img_width = len(bin_arr[0])
    img_height = len(bin_arr)

    bin_width = '{:032b}'.format(img_width)        # {:32b} -> Max image width: 4294967296 pixels (2^32)
    bin_height = '{:032b}'.format(img_height)      # {:32b} -> Max image height: 4294967296 pixels (2^32)
    img_dimension_bits = 32 + 32

    pixel_qty = img_width * img_height
    streams_qty = math.ceil( ( pixel_qty * 8 + img_dimension_bits ) / STREAM_INFORMATION_BITS_QTY )

    streams = []
    data_stream  = bin_width + bin_height
    for i in range(0, img_height):
        for j in range(0, img_width):
            if (len(data_stream) + 8 != STREAM_INFORMATION_BITS_QTY):
                data_stream += bin_arr[i][j]
            else:
                data_stream += bin_arr[i][j]
                streams.append(data_stream)
                data_stream = ""

    if (len(data_stream) != STREAM_INFORMATION_BITS_QTY):
        rest = STREAM_INFORMATION_BITS_QTY - len(data_stream)
        data_stream += "0" * rest
        streams.append(data_stream)

    for i in range(0, streams_qty):
        streams[i] = add_parity_bits_to_stream(streams[i])

    return streams

def add_parity_bits_to_stream(stream):
    """ Adds the parity bits on a data-stream.

        :param stream: stream of data where parity bits are going to be placed on.
        :return: stream of data with parity bits added.

    """
    new_stream = stream
    counter = 0
    while(counter < STREAM_LENGTH):
        if ( is_power2(counter + 1) ):
            new_stream = new_stream[0:counter] + "x" + new_stream[counter:]
        counter+= 1

    for i in range(0, STREAM_PARITY_BITS_QTY):
        position = (2**i)
        parity_value = generate_parity_value(position, new_stream)
        new_stream = new_stream[0:position-1] + parity_value + new_stream[position:]

    return new_stream

def generate_parity_value(position, stream):
    """ Obtains the parity value which is going to be positioned in a certain place on a data-stream.

        :param position: Position where the parity value is going to be placed.
        :param stream: Stream of data.
        :return: Parity value generated.

    """
    exponent = obtain_power2_exponent(position)
    ret = ""
    first_found = True
    for i in range(0, STREAM_LENGTH):
        aux = '{:01b}'.format(i+1).zfill(STREAM_PARITY_BITS_QTY)
        if(aux[-(exponent+1)] == "1"):
            if (first_found):
                first_found = False
            elif(ret == ""):
                ret = stream[i]
            else:
                ret = xor_function(ret, stream[i])
    return ret

def remove_parity_values(streams):
    """ Remove the parity values of a group of datastreams, which were previously codified with a hamming algorithm

        :param streams: list of streams of data with hamming parity values.
        :return: list of streams of data without hamming parity values.

    """

    new_streams = []
    for i in range(0, len(streams)):
        stream = streams[i]
        removed_counter = 0
        for j in range(0, STREAM_PARITY_BITS_QTY):
            position = 2**j - removed_counter - 1
            stream = stream[0:position] + stream[position+1:]
            removed_counter += 1
        new_streams.append(stream)
    return new_streams

def obtain_image_values(streams):
    """ Obtains the data inside of a group of data-streams, passing the data from bits to decimal integer, which
    are data for an image file.

        :param streams: list of streams of data as group of bits.
        :return: list of streams of data as group of decimal integers.

    """

    img_width = int(streams[0][0:32], 2)
    img_height = int(streams[0][32:64], 2)
    last_position = 64
    i = 0                                       # index of streams row
    counter = 0                                 # number of pixels decoded
    counter_limit = img_width * img_height      # limit of pixels to be decoded
    row = []                                    # row of pixels decoded
    img_data = []                               # group of row of pixels decoded

    while( counter != counter_limit):
        if (last_position == STREAM_INFORMATION_BITS_QTY):
            i += 1
            last_position = 0
        row.append(int(streams[i][last_position: last_position + 8],2))
        if (len(row) == img_width):
            img_data.append(row)
            row = []
        last_position += 8
        counter += 1

    return img_data


def decode_data_stream_to_image(streams):
    """ Decodes the data inside of a group of data-streams and creates an Image object from what is obtained.

        :param streams: list of streams of data codified.
        :return: Image object obtained from the decoded data.

    """
    new_streams = remove_parity_values(streams)
    img_data = obtain_image_values(new_streams)
    np_image_data = np.array(img_data, dtype=np.int8)
    image = Image.fromarray(np_image_data, mode="L")
    return image

def save_image(image, path):
    """ Save an image as JPEG in the specified path.

        :param image: Image object which is going to be saved.
        :param path: Path where the image is going to be saved.
        :return: Nothing.

    """
    image.save(format_image_path(path), 'JPEG')


def is_power2(num):
    """ Check if number is power of 2.

        :param num: Integer number that's going to be checked.
        :return: True if num is power of 2. False if not.

    """
    return num != 0 and ((num & (num - 1)) == 0)


def obtain_power2_exponent(num):
    """ Resolves (2^exponent = num) and obtains the exponent.

        :param num: Integer number, which is supposed to be a power of 2.
        :return: Returns the exponent in (2^exponent = num). If num is not a power of 2, then returns -1.

    """
    if (is_power2(num)):
        exponent = int(math.log(num,2))
        return exponent
    else:
        return -1


def xor_function(a, b):
    """ Applies the xor operator over the entry parameters (a and b). If the entry parameters are not "0" or "1", then
    it will return "1".

        :param a: "0" or "1".
        :param b: "0" or "1".
        :return: "0" or "1".

    """
    if ((a == "0" and b == "0") or (a == "1" and b == "1")):
        return "0"
    else:
        return "1"
