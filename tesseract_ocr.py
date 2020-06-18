# Library imports
import cv2
import pytesseract
import numpy as np

# Self-defined classes imports
import preprocessor

# Initialize tools
img = cv2.imread('images/example_01.png') # Path to image file
pre_processor = preprocessor.preprocessor() # Pre-processor

# Show pre-processed image output for debugging
def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# Process from image to string and print out
preprocessed_image = pre_processor.pre_process(img)
output = pytesseract.image_to_string(preprocessed_image)
print(output)

# Show the pre-processed image
show_image(preprocessed_image)