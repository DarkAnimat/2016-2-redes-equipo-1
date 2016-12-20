import os
from lib import codificacion as cod

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "image")

def format_image_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_IMAGE_RESOURCES, path)
        return new_path
    return path

cod.set_stream_extended_bit(True)                                                       # Set If hamming code is extended
cod.set_stream_information_bits_qty(256)                                                # Set Bits of information
cod.set_stream_parity_bits_qty(9)                                                       # Set bit of parity

image_path = format_image_path("test32x32.jpg")                                         # Path of the image used for testing
image = cod.open_image_file(image_path)                                                 # Load the Image object used for testing
encoded_image = cod.encode_image_to_data_streams(image)                                 # Encoding image as data streams
for i in range(0,len(encoded_image)):                                                   # Check if all data stream is encoded correctly
    print(encoded_image[i])
    is_ok, corrected_data_stream = cod.check_and_correct_data_stream(encoded_image[i])  # Checking Data stream with no errors
    if not(is_ok):
        print("Unexpected error has occurred")
        break
decoded_image = cod.decode_data_streams_to_image(encoded_image)                         # Decoding data streams as images
new_image_path = format_image_path("test_result.jpg")
cod.save_image(decoded_image, new_image_path)                                           # Saving decoded image as "test_result.jpg"


print("Press enter to continue with next test:")
input()

# TESTING DATA STREAM WITH A SINGLE ERROR
print("Check if codification can detect a single error and correct it")
data_stream = encoded_image[0]
if data_stream[0] == "0":
    bad_data_stream1 = "1" + data_stream[1:]
else:
    bad_data_stream1 = "0" + data_stream[1:]
print("Data-stream used for testing (Only 1 error):", bad_data_stream1)
is_ok, corrected_data_stream = cod.check_and_correct_data_stream(bad_data_stream1)
if (is_ok):
    print("Data stream has no error or had one error that could be corrected\nCorrected data stream:")
    print(corrected_data_stream)

else:
    print("Data stream has multiple errors that cannot be corrected\nUncorrected data stream:")
    print(corrected_data_stream)
print("\n\n")



print("Press enter to continue with next test:")
input()

# TESTING DATA STREAM WITH DOUBLE ERROR
print("Check if codification can detect double error and correct it")
if bad_data_stream1[1] == "0":
    bad_data_stream2 = bad_data_stream1[0] + "1" + bad_data_stream1[2:]
else:
    bad_data_stream2 = bad_data_stream1[0] + "0" + bad_data_stream1[2:]
print("Data-stream used for testing (2 errors):", bad_data_stream2)
is_ok, corrected_data_stream = cod.check_and_correct_data_stream(bad_data_stream2)

if (is_ok):
    print("Data stream has no error or had one error that could be corrected\nCorrected data stream:")
    print(corrected_data_stream)

else:
    print("Data stream has multiple errors that cannot be corrected\nUncorrected data stream:")
    print(corrected_data_stream)
