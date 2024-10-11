
import numpy as np
import matplotlib.pyplot as plt
class Image_analyzer():
    def __init__(self , image_path = None):
        self.image_path = image_path
        self.image_array = None
        self.width = None
        self.height = None
        self.max_pixel_value = None
        
    def mypgmread(self, image_path = None):
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
    def mypgmwrite(self, width = None, height = None, max_pixel_value = None, image_array = None ,image_path = None):
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
    
    
    def myImageCorrelation(self, kernel):
        g = np.zeros((self.height, self.width))
        kernel_height, kernel_width = kernel.shape
        for x in range (self.height):
            for y in range(self.width):
                for s in range(-kernel_height//2,kernel_height//2):
                    for t in range(-kernel_width//2,kernel_width//2):
                        if x+s >= 0 and x+s < self.height and y+t >= 0 and y+t < self.width:
                            g[x][y] += kernel[s][t] * self.image_array[x+s][y+t]                    
        return g
    
    
    
    # Image scaling between 0 and 255
    def image_array_scale(self, image_array: np.ndarray):
        if np.min(image_array) < 0:
            image_array = image_array + abs( np.min(image_array))
        if np.min(image_array) > 0:
            image_array = image_array - np.min(image_array)
        
        #linear scale according to the max pixel value
        image_array = image_array * 255 / np.max(image_array)
        #convert to integer
        image_array = np.array(image_array, dtype=np.uint8)
        return image_array
    
    def myImageNegative(self):
        return self.max_pixel_value - self.image_array

    def myImageLogTransform(self, c = 1):
        return (c * np.log(np.ones(self.image_array.shape) + self.image_array))
    
    def myImageGammaTransform(self, gamma = 1, c = 1):
        return (c * np.power(self.image_array, gamma))
    
    def myImageMedianFilter(self, kernel_size = 3):
        g = np.zeros((self.height, self.width))
        for x in range (self.height):
            for y in range(self.width):
                values = []
                for s in range(-kernel_size//2,kernel_size//2):
                    for t in range(-kernel_size//2,kernel_size//2):
                        if x+s >= 0 and x+s < self.height and y+t >= 0 and y+t < self.width:
                            values.append(self.image_array[x+s][y+t])
                g[x][y] = np.median(values)
        return g
    
    def myImageHistogramEqualization(self):
        g = np.zeros((self.height, self.width))
        hist, bins = np.histogram(self.image_array.flatten(),256,[0,256])
        cdf = hist.cumsum()
        cdf_normalized = cdf * hist.max()/ cdf.max()
        for x in range (self.height):
            for y in range(self.width):
                g[x][y] = cdf_normalized[self.image_array[x][y]]
        return g
    
    def get_gaussian_filter(self, size, sigma):
        filter = np.zeros((size, size))
        for x in range(size):
            for y in range(size):
                filter[x][y] = np.exp(-((x - size//2)**2 + (y - size//2)**2) / (2 * sigma**2))
        return filter/np.sum(filter)
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
    
    
        