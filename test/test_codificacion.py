import os
from lib import codificacion as cod

PATH_MAIN = os.path.normpath(os.getcwd())
PATH_IMAGE_RESOURCES = os.path.join(PATH_MAIN, "..", "resources", "image")

def format_image_path(path):
    if not(os.path.isabs(path)):
        new_path = os.path.join(PATH_IMAGE_RESOURCES, path)
        return new_path
    return path


image_path = format_image_path("test32x32.jpg")      # Path of the image used for testing
image = cod.open_image_file(image_path)        # Load the Image object used for testing

print("")
print("\t\t===================================================")
print("\t\t         TESTING ENCODING AND DECODING             ")
print("\t\t===================================================")
print("")

print(">>> Encoding image...   ")
encoded_image = cod.encode_image_to_data_streams(image)             # Encoding image as data streams
print("Ready\n")

print(">>> Decoding image...   ")
decoded_image = cod.decode_data_streams_to_image(encoded_image)     # Decoding data streams as images
print("Ready\n")

print(">>> Saving decoded image as test_result.jpg")
new_image_path = format_image_path("test_result.jpg")
cod.save_image(decoded_image, new_image_path)                       # Saving decoded image as "test_result.jpg"
print("Ready\n")


print("")
print("\t\t===================================================")
print("\t\t       TESTING VALIDATION AND ERROR HANDLING       ")
print("\t\t===================================================")
print("")


# TESTING DATA STREAM WITH NO ERROR
data_stream  = encoded_image[0]                                     # Data stream used for testing (No errors)
print("Data-stream used for testing (No errors):")
print(data_stream)
is_ok, corrected_data_stream = cod.check_and_correct_data_stream(data_stream)  # Checking Data stream with no errors
if (is_ok):
    print(">>> Data stream has no error or had one error that could be corrected")
    print(">>> Corrected data stream:")
    print(corrected_data_stream)

else:
    print(">>> Data stream has multiple errors that cannot be corrected")
    print(">>> Uncorrected data stream:")
    print(corrected_data_stream)

print("\n\n")


# TESTING DATA STREAM WITH A SINGLE ERROR
if data_stream[0] == "0":
    bad_data_stream1 = "1" + data_stream[1:]
else:
    bad_data_stream1 = "0" + data_stream[1:]
print("Data-stream used for testing (Only 1 error):")
print(bad_data_stream1)
is_ok, corrected_data_stream = cod.check_and_correct_data_stream(bad_data_stream1)
if (is_ok):
    print(">>> Data stream has no error or had one error that could be corrected")
    print(">>> Corrected data stream:")
    print(corrected_data_stream)

else:
    print(">>> Data stream has multiple errors that cannot be corrected")
    print(">>> Uncorrected data stream:")
    print(corrected_data_stream)

print("\n\n")

# TESTING DATA STREAM WITH DOUBLE ERROR
if bad_data_stream1[1] == "0":
    bad_data_stream2 = bad_data_stream1[0] + "1" + bad_data_stream1[2:]
else:
    bad_data_stream2 = bad_data_stream1[0] + "0" + bad_data_stream1[2:]
print("Data-stream used for testing (2 errors):")
print(bad_data_stream2)
is_ok, corrected_data_stream = cod.check_and_correct_data_stream(bad_data_stream2)
if (is_ok):
    print(">>> Data stream has no error or had one error that could be corrected")
    print(">>> Corrected data stream:")
    print(corrected_data_stream)

else:
    print(">>> Data stream has multiple errors that cannot be corrected")
    print(">>> Uncorrected data stream:")
    print(corrected_data_stream)
