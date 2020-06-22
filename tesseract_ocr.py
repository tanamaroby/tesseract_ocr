# Library imports
import cv2
import pytesseract
import numpy as np

# Self-defined classes imports
import preprocessor
import imageboxer

# Initialize tools
img = cv2.imread('images/example_01.png') # Path to image file
pre_processor = preprocessor.preprocessor() # Pre-processor
image_boxer = imageboxer.imageboxer()

# Process from image to string and print out
preprocessed_image = pre_processor.pre_process(img)
boxed_image = image_boxer.box_image(img)
output = pytesseract.image_to_string(preprocessed_image)
print(output)

# Show pre-processed image output for debugging
cv2.imshow("preprocessed_image", preprocessed_image)
cv2.imshow("boxed_image", boxed_image)
cv2.waitKey(0)