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
plt.figure(1)
plt.imshow(image_array, cmap='gray')

#write the image to a new file
analyzer.draw_horizontal_line(100,120)
#analyzer.image_write(width, height, max_pixel_value,image_array, file_dir+'/'+'prague_copy.pgm')

plt.figure(2)
analyzer.show_image()


plt.show()