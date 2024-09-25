
import numpy as np
import matplotlib.pyplot as plt
class Image_analyzer():
    def __init__(self):
        pass
    def image_read(self, image_path):
        # Read pgm image from file
        with open(image_path, 'rb') as f:
            # Read the header of the image
            first_line = f.readline()
            # Check if the image is in P5 format
            if first_line != b'P5\n':
                raise ValueError('Image format not supported' + str(first_line))
            # Read the next lines and check for comments and ignore them
            second_line = f.readline()
            while second_line[0] == 35: # 35 is the ascii code for #
                second_line = f.readline()
            # Read the image width and height values
            width_and_height_line = second_line
            width_and_height = width_and_height_line.split()
            width, height = int(width_and_height[0]), int(width_and_height[1])
            # Read the max pixel value
            max_pixel_value_line = f.readline()
            max_pixel_value = int(max_pixel_value_line)
            # Read the image data
            image_data = f.read()
            # Create a numpy array from the image data
            image_array = np.frombuffer(image_data, dtype=np.uint8)
            # Reshape the image to matrix
            image_array = image_array.reshape((height, width))
            return image_array, width, height, max_pixel_value
    def image_write(self, image_array, width, height, max_pixel_value, image_path):
        # Write pgm image to file
        with open(image_path, 'wb') as f:
            # Write the header of the image
            f.write(b'P5\n')
            # Write the width and height of the image
            f.write(b'%d %d\n' % (width, height))
            # Write the max pixel value
            f.write(b'%d\n' % max_pixel_value)
            # Write the image data
            f.write(image_array.tobytes())
        print('Image written to:', image_path)
        