import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

KNOWN_AREA_A4_CM2 = 623.7  # The known area of an A4 sheet in square centimeters

def find_largest_contour(contours):
    max_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour
    return largest_contour if largest_contour is not None else np.array([])

def calculate_scale_factor(pixel_area_a4):
    return KNOWN_AREA_A4_CM2 / pixel_area_a4

def save_scale_factor(scale_factor, file_path='AreaContour/scale_factor.txt'):
    with open(file_path, 'w') as file:
        file.write(str(scale_factor))
        print("Scale factor saved successfully.")

def choose_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title='Choose up to 5 images containing A4 paper', 
                                             filetypes=[('Image Files', '*.jpeg *.jpg *.png')], 
                                             initialdir='./',
                                             multiple=True)
    return file_paths[:5]

def display_image_with_contour(image, contour, scale_factor, image_path):
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 30)  # Draw contour in green
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f'Scale Factor: {scale_factor} cm²/px²')
    plt.axis('off')
    plt.show()

def process_images(image_paths):
    scale_factors = []
    for image_path in image_paths:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(blurred, 150, 350)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = find_largest_contour(contours)
        if largest_contour is not None:
            pixel_area_a4 = cv2.contourArea(largest_contour)
            scale_factor = calculate_scale_factor(pixel_area_a4)
            scale_factors.append(scale_factor)
            display_image_with_contour(image, largest_contour, scale_factor, image_path)
        else:
            print("A4 paper not detected in image:", image_path)
    if scale_factors:
        average_scale_factor = sum(scale_factors) / len(scale_factors)
        save_scale_factor(average_scale_factor)

def main():
    image_paths = choose_files()
    if image_paths:
        process_images(image_paths)
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()
