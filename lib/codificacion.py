import numpy as np
import math
from PIL import Image


# Encoding info:
STREAM_INFORMATION_BITS_QTY = 256  # Quantity of bits used for storing information on a data-stream
STREAM_PARITY_BITS_QTY = 9         # Quantity of bits used for parity values on a data-stream
STREAM_LENGTH = STREAM_INFORMATION_BITS_QTY + STREAM_PARITY_BITS_QTY  # Quantity of bits on a data-stream
STREAM_EXTENDED_BIT = True          # Extra bit for extended hamming code?
if STREAM_EXTENDED_BIT: STREAM_LENGTH += 1

def set_stream_information_bits_qty(value):
    """ Set the quantity of bits used for storing information in Hamming algorithm

    :param value: Value to set
    :return: Nothing
    """
    global STREAM_INFORMATION_BITS_QTY
    global STREAM_LENGTH
    STREAM_INFORMATION_BITS_QTY = value
    STREAM_LENGTH = STREAM_INFORMATION_BITS_QTY + STREAM_PARITY_BITS_QTY
    if STREAM_EXTENDED_BIT: STREAM_LENGTH += 1


def set_stream_parity_bits_qty(value):
    """ Set the quantity of parity bits used for storing information in Hamming algorithm. Must follow the next
    relationship:

            2^k - 1 >= k + n

    where:
    k = number of parity bits
    n = number of information bits

    If relationship is not made, then Hamming algorithm won't work.

    :param value: Value to set
    :return: Nothing

    """
    global STREAM_PARITY_BITS_QTY
    global STREAM_LENGTH
    STREAM_PARITY_BITS_QTY = value
    STREAM_LENGTH = STREAM_INFORMATION_BITS_QTY + STREAM_PARITY_BITS_QTY
    if STREAM_EXTENDED_BIT: STREAM_LENGTH += 1


def set_stream_extended_bit(value):
    """ Set true or false to use extended Hamming algorithm or  not

    :param value: True or False
    :return: Nothing

    """
    global STREAM_EXTENDED_BIT
    global STREAM_LENGTH
    STREAM_EXTENDED_BIT = value
    STREAM_LENGTH = STREAM_INFORMATION_BITS_QTY + STREAM_PARITY_BITS_QTY
    if STREAM_EXTENDED_BIT: STREAM_LENGTH += 1


def open_image_file(path):
    """ Open an image file if possible and returns and Image object

    :param path: Path of the image to be opened
    :return: Image object if the image can be opened, None if not

    """
    try:
        image = Image.open(path).convert('L')
        return image
    except IOError:
        print("Error: File cannot be found, or the image cannot be opened and identified.")
        print("Source: '{}'\n".format(path))
        return None


def encode_image_to_data_streams(image):
    """ Encode and convert an Image object to an array of data-streams

        :param image: Image object to be encoded
        :return: array of data-streams (array of strings with bytes as string)

    """

    # Image properties:
    image_as_array = np.array(image)
    image_height, image_width = image_as_array.shape
    pixel_qty = image_width * image_height

    # Data stream properties:
    bin_width = '{:032b}'.format(image_width)    # {:32b} -> Max image width: 4294967296 pixels (2^32)
    bin_height = '{:032b}'.format(image_height)  # {:32b} -> Max image height: 4294967296 pixels (2^32)
    img_dimension_bits = 32 + 32                 # Quantity of bits for storing the width and height of the image
    streams_qty = math.ceil((pixel_qty * 8 + img_dimension_bits) / STREAM_INFORMATION_BITS_QTY)

    # Generating the data streams:
    streams = []
    data_stream = bin_width + bin_height
    for i in range(0, image_height):
        for j in range(0, image_width):
            data_stream_length = len(data_stream)
            if data_stream_length + 8 != STREAM_INFORMATION_BITS_QTY:
                data_stream += '{:08b}'.format(image_as_array[i][j])
            elif data_stream_length + 8 == STREAM_INFORMATION_BITS_QTY:
                data_stream += '{:08b}'.format(image_as_array[i][j])
                streams.append(data_stream)
                data_stream = ""
    if len(data_stream) != STREAM_INFORMATION_BITS_QTY and len(data_stream) != 0:
        rest = STREAM_INFORMATION_BITS_QTY - len(data_stream)
        data_stream += "0" * rest
        streams.append(data_stream)

    # Adding parity bits according to Hamming algorithm:
    for i in range(0, streams_qty):
        streams[i] = add_parity_bits_to_stream(streams[i])

    encoded_image = np.array(streams)
    return encoded_image


def add_parity_bits_to_stream(stream):
    """ Adds the parity bits on a data-stream.

        :param stream: stream of data where parity bits are going to be placed on.
        :return: stream of data with parity bits added.

    """
    new_stream = stream
    limit = STREAM_LENGTH

    if STREAM_EXTENDED_BIT: limit = limit - 1
    for i in range(0, limit):
        if is_power2(i + 1):
            new_stream = new_stream[0:i] + "x" + new_stream[i:]
    if STREAM_EXTENDED_BIT: new_stream = new_stream + "x"


    for i in range(0, STREAM_PARITY_BITS_QTY):
        position = (2**i)
        parity_value = generate_parity_value(position, new_stream)
        new_stream = new_stream[0:position-1] + parity_value + new_stream[position:]

    if STREAM_EXTENDED_BIT:
        extended_bit = generate_extended_parity_value(new_stream)
        new_stream = new_stream[0:-1] + extended_bit

    return new_stream


def generate_parity_value(position, stream):
    """ Obtains the parity value which is going to be positioned in a certain place on a data-stream.

        :param position: Position where the parity value is going to be placed.
        :param stream: Stream of data.
        :return: Parity value generated.

    """

    exponent = obtain_power2_exponent(position)
    #print("exponent", exponent, -(exponent+1))
    ret = ""
    first_found = True
    limit = STREAM_LENGTH
    if STREAM_EXTENDED_BIT: limit = limit - 1
    for i in range(0, limit):
        aux = '{:01b}'.format(i+1).zfill(STREAM_PARITY_BITS_QTY)
        aux_index = STREAM_PARITY_BITS_QTY - exponent - 1
        if (aux[aux_index] == "1"):
            if first_found:
                first_found = False
            elif ret == "":
                ret = stream[i]

            else:
                ret = xor_function(ret, stream[i])

    return ret

def generate_extended_parity_value(stream):
    """ Generate the extra parity value for extended hamming code

        :param stream: Stream of data.
        :return: Extended parity value.

    """
    ret = ""
    for i in range(0, STREAM_LENGTH - 1):
        if i == 0:
            ret = stream[i]
        else:
            ret = xor_function(ret, stream[i])
    return ret


def remove_parity_values(streams):
    """ Remove the parity values of a group of data-streams, which were previously codified with a hamming algorithm

        :param streams: list of streams of data with hamming parity values.
        :return: list of streams of data without hamming parity values.

    """

    new_streams = []
    for i in range(0, len(streams)):
        stream = streams[i]
        removed_counter = 0
        if STREAM_EXTENDED_BIT:
            stream = stream[0:-1]
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

    while counter != counter_limit:
        if last_position == STREAM_INFORMATION_BITS_QTY:
            i += 1
            last_position = 0
        row.append(int(streams[i][last_position: last_position + 8], 2))
        if len(row) == img_width:
            img_data.append(row)
            row = []
        last_position += 8
        counter += 1

    return img_data


def decode_data_streams_to_image(streams):
    """ Decodes the data inside of a group of data-streams and creates an Image object from what is obtained.

        :param streams: list of streams of data codified.
        :return: Image object obtained from the decoded data.

    """
    new_streams = remove_parity_values(streams)
    img_data = obtain_image_values(new_streams)
    np_image_data = np.array(img_data, dtype=np.int8)
    image = Image.fromarray(np_image_data, mode="L")
    return image



def check_and_correct_data_stream(stream):
    """ Check if a data stream is encoded correctly. If not, tries to correct it
        :param stream: Stream of data, encoded with hamming algorithm
        :return: Returns a Tuple.
                 1) True if data is encoded correctly or if code was corrected, False if not.
                 2) stream (Corrected if necessary and possible)
    """

    # Obtaining parity values
    C = ""
    for i in range(0, STREAM_PARITY_BITS_QTY):
        position = (2**i)
        parity_value = generate_parity_value(position, stream)
        if (stream[position-1] == parity_value):
            C += "0"
        else:
            C += "1"

    C = int(C[::-1], 2) - 1


    # Does not continue if extended hamming code is not available
    if not(STREAM_EXTENDED_BIT):

        # No error occurred
        if (C == -1):
            return True, stream

        # An error has ocurred or multiple error has occurred. Correction will not be made.
        else:
            return False, stream

    else:
        extended_value = generate_extended_parity_value(stream)
        if (stream[-1] == extended_value):
            P = 0
        else:
            P = 1

        # No error occurred
        if ( C == -1 and P == 0 ):
            return True, stream

        # Error could not be detected
        if ( C >= len(stream)):
            return False, stream

        # A single error occurred that can be corrected
        elif ( C != -1 and P == 1):
            if (stream[C] == "0"):
                return True, stream[0:C] + "1" + stream[C+1:]
            elif(stream[C] == "1"):
                return True, stream[0:C] + "0" + stream[C+1:]

        # A double error occurred that is detected but cannot be corrected
        elif ( C != -1 and P == 0):
            return False, stream

        # An error occurred in the last bit, can be corrected.
        elif ( C == -1 and P == 1):
            if (stream[-1] == "0"):
                return True, stream[0:-1] + "1"
            elif(stream[-1] == "1"):
                return True, stream[0:-1] + "0"


def save_image(image, path):
    """ Save an image as JPEG in the specified path.

        :param image: Image object which is going to be saved.
        :param path: Path where the image is going to be saved.
        :return: Nothing.

    """
    image.save(path, 'JPEG')


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
    if is_power2(num):
        exponent = int(math.log(num, 2))
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
    if (a == "0" and b == "0") or (a == "1" and b == "1"):
        return "0"
    else:
        return "1"
