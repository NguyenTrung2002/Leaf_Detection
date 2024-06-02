import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

def load_scale_factor(file_path='AreaContour/scale_factor.txt'):
    try:
        with open(file_path, 'r') as file:
            scale_factor = float(file.read())
            print("Scale factor loaded successfully.")
            return scale_factor
    except FileNotFoundError:
        print("Scale factor file not found.")
        return None

def apply_green_color_filter(image):
    # Apply Gaussian blur to smooth the image, reducing noise and improving edge detection
    blurred_image = cv2.GaussianBlur(image, (11, 11), 0)
    
    # Convert to HSV color space after blurring
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 50, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    # Use morphological operations to clean up the mask
    
    return mask

def find_largest_contour(contours):
    max_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour
    return largest_contour

def find_precise_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def calculate_leaf_area(contour, scale_factor):
    if contour is not None:
        area = cv2.contourArea(contour)
        real_area = area * scale_factor
        return real_area
    return 0

def display_images(image_path, scale_factor):
    image = cv2.imread(image_path)
    if image is not None:
        mask = apply_green_color_filter(image)
        contours = find_precise_contours(mask)
        largest_contour = find_largest_contour(contours)
        total_leaf_area = calculate_leaf_area(largest_contour, scale_factor)
        
        if largest_contour is not None:
            cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
        
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(f'Processed Image with Largest Leaf Area: {total_leaf_area:.2f} cm²')
        plt.axis('off')
        plt.show()
    else:
        print("No file selected.")

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Choose an image file',
                                           filetypes=[('Image Files', '*.jpeg *.jpg *.png')],
                                           initialdir='./')
    if file_path:
        scale_factor = load_scale_factor()
        if scale_factor:
            display_images(file_path, scale_factor)
        else:
            print("Scale factor not found, please run scale_factor_calculator.py first.")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
