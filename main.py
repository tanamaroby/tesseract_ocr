# Library imports
import cv2
import pytesseract
import numpy as np
from pdf2image import convert_from_path

# Self-defined classes imports
import imagepreprocessor
import imageboxer
import imageorientation
import idprocessor
import crop

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Converting PDF to PNG when necessary
filepath = 'documents/PANCard3.jpeg'

# Checking if the file given is PDF or Image format
if ('.pdf' in filepath):
    # In the case of multiple pages
    pages = convert_from_path(filepath)
    image_counter = 1
    for page in pages:
        filename = "page_" + str(image_counter) + ".png"
        page.save('images/' + filename, 'PNG')
        image_counter = image_counter + 1

    # Initialize tools
    img = cv2.imread('images/page_1.png') # Path to image file

else:
    img = cv2.imread(filepath)


image_preprocessor = imagepreprocessor.imagepreprocessor() # Pre-processor
image_boxer = imageboxer.imageboxer() # Boxer
image_orientation = imageorientation.imageorientation() # Detect orientation
image_cropper = crop.crop() # Cropping tool

output_postprocessor = idprocessor.idprocessor() # Process the output


# Crop the image
cropped_image = image_cropper.crop(img) 

# Process from image to string 
preprocessed_image = image_preprocessor.preprocess(cropped_image)
boxed_image = image_boxer.box_image(cropped_image)


output = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6')

# Processing the output
processedoutput = output_postprocessor.postprocess(output)

# Writing into file for documentation   
with open('generated/text/rawoutput.txt', 'w+') as file:
    file.write(output)
    file.close()

# Writing processed output 
with open('generated/text/processedoutput.txt', 'w+') as file:
    file.write(processedoutput)
    file.close()

# Save preprocessed images for debugging
cv2.imwrite("generated/images/preprocessed_image.png", preprocessed_image)
cv2.imwrite("generated/images/boxed_image.png", boxed_image)
cv2.imwrite("generated/images/cropped_image.png", cropped_image)

