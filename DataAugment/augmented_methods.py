import tkinter as tk
from tkinter import filedialog
import cv2
from numpy import expand_dims
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from matplotlib import pyplot as plt
import os

def select_images():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()  # Returns a tuple of selected file paths
    return file_paths

def augment_image(image_path, augment_type):
    img = load_img(image_path)
    img = img_to_array(img)
    data = expand_dims(img, 0)
    
    if augment_type == 'brightness':
        generator = ImageDataGenerator(brightness_range=[0.5, 2.0])
    elif augment_type == 'flip':
        generator = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)
    elif augment_type == 'rotate':
        generator = ImageDataGenerator(rotation_range=90)
    elif augment_type == 'shift':
        generator = ImageDataGenerator(width_shift_range=[-150, 150])
    elif augment_type == 'zoom':
        generator = ImageDataGenerator(zoom_range=[0.5, 2.0])
    elif augment_type == 'shear':
        generator = ImageDataGenerator(shear_range=45)
    else:
        return
    
    gen = generator.flow(data, batch_size=1)
    # plt.figure(figsize=(10, 10))  # Set the figure size for better visualization
    output_folder = "D:/Leaf/DataAugment/ImageDataGenerator/"
    for i in range(9):
        # plt.subplot(330 + 1 + i)
        batch = gen.next()
        image = batch[0].astype('uint8')
        # plt.imshow(image)
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # Create the output file path
        file_name = os.path.basename(image_path)  # Get the base name of the file
        file_name_no_ext = os.path.splitext(file_name)[0]  # Remove the extension
        output_path = os.path.join(output_folder, f"{file_name_no_ext}_{augment_type}_{i}.png")
        cv2.imwrite(output_path, image_bgr)
    plt.show()

if __name__ == '__main__':
    image_paths = select_images()
    if image_paths:
        for image_path in image_paths:
            print(f"Selected image: {image_path}")
            augment_image(image_path, 'brightness')
            augment_image(image_path, 'flip')
            augment_image(image_path, 'rotate')
            augment_image(image_path, 'shear')
            augment_image(image_path, 'shift')
            augment_image(image_path, 'zoom')
    else:
        print("No images selected.")