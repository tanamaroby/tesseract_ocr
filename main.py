# Library imports
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path

# Self-defined classes imports
import imagepreprocessor
import imageboxer
import imageorientation

# Converting PDF to PNG when necessary
pages = convert_from_path('documents/Invoice.pdf')

# In the case of multiple pages
image_counter = 1
for page in pages:
    filename = "page_" + str(image_counter) + ".png"
    page.save('images/' + filename, 'PNG')
    image_counter = image_counter + 1

# Initialize tools
img = cv2.imread('images/page_1.png') # Path to image file
image_preprocessor = imagepreprocessor.imagepreprocessor() # Pre-processor
image_boxer = imageboxer.imageboxer() # Boxer
image_orientation = imageorientation.imageorientation() # Detect orientation

# Process from image to string and write into file
preprocessed_image = image_preprocessor.preprocess(img)
boxed_image = image_boxer.box_image(img)
output = pytesseract.image_to_string(preprocessed_image)

# Detect skew
image_orientation.detect_angle(img)

with open('generated/text/output.txt', 'w') as file:
    file.write(output)

# Save preprocessed images for debugging
cv2.imwrite("generated/images/preprocessed_image.png", preprocessed_image)
cv2.imwrite("generated/images/boxed_image.png", boxed_image)