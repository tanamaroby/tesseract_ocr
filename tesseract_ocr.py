# Imports
import cv2
import pytesseract

# Path to image file
img = cv2. imread('images/example_01.png')

# Process from image to string
pytesseract.image_to_string(img)