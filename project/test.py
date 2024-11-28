import cv2
import os
import matplotlib.pyplot as plt

# Load Haarcascade file
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
if not os.path.exists(cascade_path):
    print(f"Error: Haarcascade file not found at {cascade_path}")
else:
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Read and process image
    
    # Get current directory
    my_dir = os.getcwd()

    # Set image path
    img_path = os.path.join(my_dir, 'project','Test_images', 'man.jpg')
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print(f"Error: Image file not found at {img_path}")
    else:
        # Detect faces
        faces = face_cascade.detectMultiScale(img, 1.1, 4)

        # Draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), 255, 2)

        # Show image
        plt.imshow(img, cmap='gray')
        plt.show()
