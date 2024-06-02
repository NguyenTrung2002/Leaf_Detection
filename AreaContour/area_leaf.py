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
    blurred_image = cv2.GaussianBlur(image, (11, 11), 0)
    # Convert to HSV color space after blurring
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 50, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
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

def process_images(image_paths, scale_factor):
    largest_areas = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        mask = apply_green_color_filter(image)
        all_contours = find_precise_contours(mask)
        largest_contour = find_largest_contour(all_contours)
        if largest_contour is not None:
            area = cv2.contourArea(largest_contour)
            real_area = area * scale_factor
            largest_areas.append(real_area)

    if largest_areas:
        average_leaf_area = sum(largest_areas) 
        print(f"Average Leaf Area of Largest Contours: {average_leaf_area:.2f} cm²")

def choose_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title='Choose up to 5 images containing leaves', 
                                             filetypes=[('Image Files', '*.jpeg *.jpg *.png')], 
                                             initialdir='./',
                                             multiple=True)
    return file_paths[:10]

def main():
    scale_factor = load_scale_factor()
    if scale_factor:
        image_paths = choose_files()
        if image_paths:
            process_images(image_paths, scale_factor)
        else:
            print("No files selected.")
    else:
        print("Scale factor not found")

if __name__ == "__main__":
    main()
