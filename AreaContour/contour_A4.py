import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

def find_largest_contour(contours):
    max_area = 0
    largest_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour
    return largest_contour

def choose_files():
    root = tk.Tk()
    root.withdraw()  # we don't want a full GUI, so keep the root window from appearing
    file_paths = filedialog.askopenfilenames(title='Choose images', 
                                             filetypes=[('Image Files', '*.jpeg *.jpg *.png')], 
                                             initialdir='./')
    return file_paths

def process_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(blurred, 150, 350)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = find_largest_contour(contours)

    if largest_contour is not None:
        # Draw the contour on the image
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)  # Draw in green
        # Show the image
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(f'Processed Image with A4 Contour: {image_path}')
        plt.show()
    else:
        print(f"No A4 paper detected in {image_path}.")

def main():
    file_paths = choose_files()
    if file_paths:
        for file_path in file_paths:
            process_image(file_path)
    else:
        print("No files selected.")

if __name__ == "__main__":
    main()
