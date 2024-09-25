from image_analyzer import Image_analyzer
import os
import matplotlib.pyplot as plt
file_dir = os.path.dirname(__file__)
#read prague.pgm image
analyzer = Image_analyzer()
image_array, width, height, max_pixel_value = analyzer.image_read(file_dir+'/'+'prague.pgm')
print('Image array:', image_array)
print('Width:', width)
print('Height:', height)
print('Max pixel value:', max_pixel_value)

#show the image using matplotlib
plt.imshow(image_array, cmap='gray')
plt.show()

#write the image to a new file
analyzer.image_write(width, height, max_pixel_value,image_array, file_dir+'/'+'prague_copy.pgm')
