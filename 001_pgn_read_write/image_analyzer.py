
import numpy as np
import matplotlib.pyplot as plt
class Image_analyzer():
    def __init__(self , image_path = None):
        self.image_path = image_path
        self.image_array = None
        self.width = None
        self.height = None
        self.max_pixel_value = None
        
    def image_read(self, image_path = None):
        if image_path == None and self.image_path == None:
            raise ValueError('Please provide an image path')
        if image_path == None:
            image_path = self.image_path
        print('Reading image from:', image_path)
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
            self.image_array = image_array.copy()
            self.width = width
            self.height = height
            self.max_pixel_value = max_pixel_value
            return image_array, width, height, max_pixel_value
    def image_write(self, width = None, height = None, max_pixel_value = None, image_array = None ,image_path = None):
        if width == None and self.width == None:
            raise ValueError('Please provide a width value or read an image first')
        elif width == None:
            width = self.width
        if height == None and self.height == None:
            raise ValueError('Please provide a height value or read an image first')
        elif height == None:
            height = self.height
        if max_pixel_value == None and self.max_pixel_value == None:
            raise ValueError('Please provide a max pixel value or read an image first')
        elif max_pixel_value == None:
            max_pixel_value = self.max_pixel_value
        image_array = np.array(image_array)
        if image_array.all() is None and self.image_array.all() is None:
            raise ValueError('Please provide an image array or read an image first')
        elif image_array.all() is None:
            image_array = self.image_array
        try :
            if image_array == None and self.image_array == None:
                raise ValueError('Please provide an image array')
        except:
            pass
        try :
            if image_array == None:
                image_array = self.image_array
        except:
            pass
        
        
        
        
        if image_path == None and self.image_path == None:
            raise ValueError('Please provide an image path')
        if image_path == None:
            image_path = self.image_path
        self.width = width
        self.height = height
        self.max_pixel_value = max_pixel_value
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
    def draw_straight_line(self, x1, x2, y1, y2,):
        if  self.image_array.all() is None:
            raise ValueError('Please read an image first')
        #check out bounds of the image array
        if  x1 < 0 or x1 > self.height      \
            or x2 < 0 or x2 > self.height   \
            or y1 < 0 or y1 > self.width  \
            or y2 < 0 or y2 > self.width:
            raise ValueError('Coordinates out of bounds')
        for i in range(x1, x2):
            for j in range(y1, y2):
                self.image_array[i][j] = 0 
    def draw_vertical_line(self, y1, y2):
        self.draw_straight_line(0, self.height, y1, y2)
    def draw_horizontal_line(self, x1, x2):
        self.draw_straight_line(x1, x2, 0 , self.width)
        
    #Illustration functions
    def show_image(self):
        if  self.image_array.all() is None:
            raise ValueError('Please read an image first or use show_image_from_array')
        plt.imshow(self.image_array, cmap='gray', vmin=0, vmax=255)
    def show_image_from_array(self, image_array):
        plt.imshow(image_array, cmap='gray', vmin=0, vmax=255)
    
        
    # Getters and setters
    def get_image_path(self):
        return self.image_path
    def set_image_path(self, image_path):
        self.image_path = image_path
    def get_image_array(self):
        return self.image_array
    def get_image_width(self):
        return self.width
    def set_image_width(self, width):
        self.width = width
    def get_image_height(self):
        return self.height
    def set_image_height(self, height):
        self.height = height
    
    
        