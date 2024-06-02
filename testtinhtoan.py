# Complete integrated code from scratch to:
# 1. Load the original image.
# 2. Apply a color filter to find the green leaf contour.
# 3. Find the largest contour, assumed to be the A4 paper.
# 4. Draw both contours on the image.
# 5. Calculate the real-world area of the leaf using the A4 paper as reference.
# 6. Display both the original and processed images side by side.

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Constants for known values
KNOWN_AREA_A4_CM2 = 623.7  # The known area of an A4 sheet in square centimeters

# Function definitions
def apply_green_color_filter(image):
    blurred_image = cv2.GaussianBlur(image, (11, 11), 0)
    # Convert to HSV color space after blurring
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 50, 40])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    return mask

def find_contours(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours
def find_largest_contour(contours):
    # Assuming the largest contour is the A4 paper
    max_area = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            largest_contour = contour
    return largest_contour

def calculate_real_world_area(pixel_area_leaf, pixel_area_a4, known_area_a4):
    # Calculate the real-world area of the leaf
    return (pixel_area_leaf * known_area_a4) / pixel_area_a4

# Load the original image
image_path = 'la90cm.jpg'
original_image = cv2.imread(image_path)

# Apply green color filter to find the green leaf
mask = apply_green_color_filter(original_image)
leaf_contours = find_contours(mask)


# Find all contours for the largest one, assumed to be the A4 paper
gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (7, 7), 0)
edged = cv2.Canny(blurred, 150, 350)
all_contours = find_contours(edged)
largest_contour = find_largest_contour(all_contours)

# Draw the contours on the image
processed_image = original_image.copy()
cv2.drawContours(processed_image, leaf_contours, -1, (0, 255, 0), 5)  # Draw the leaf contour in green
cv2.drawContours(processed_image, [largest_contour], -1, (0, 0, 255), 5)  # Draw the A4 contour in red

# Calculate the areas
pixel_area_a4 = cv2.contourArea(largest_contour)
# pixel_area_leaf = cv2.contourArea(leaf_contours)
total_pixel_area_green = sum(cv2.contourArea(contour) for contour in leaf_contours)
real_world_area_leaf = calculate_real_world_area(total_pixel_area_green, pixel_area_a4, KNOWN_AREA_A4_CM2)

# Display both the original and processed images
plt.figure(figsize=(10, 20))

# Original image
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

# Processed image with areas
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB))
plt.title(f'Processed Image\nLeaf Area: {real_world_area_leaf:.2f} cm²')
plt.axis('off')

plt.tight_layout()
plt.show()

# Return the real world area of the leaf
real_world_area_leaf
