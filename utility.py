import cv2
from pdf2image import convert_from_path
import os

def get_paths(filepath):
    file_paths = list()
    ## Checking if the file given is PDF or Image format
    #if ('.pdf' in filepath):
    #    # In the case of multiple pages
    #    pages = convert_from_path(filepath)
    #    image_counter = 1
    #    for page in pages:
    #        filename = "page_" + str(image_counter) + ".png"
    #        page.save('generated/images/' + filename, 'PNG')
    #        image_counter = image_counter + 1
    #        file_paths.append('generated/images/' + filename)
    #else:
    #    file_paths.append(filepath)

    file_paths.append(filepath)
    return file_paths

def save_output(output, processed_output, fn):
    # Writing into file for documentation
    with open('generated/text/' + fn + 'rawoutput.txt', 'w+') as file:
        file.write(output)
        file.close()
    # Writing processed output
    with open('generated/text/' + fn + 'processedoutput.txt', 'w+') as file:
        file.write(processed_output)
        file.close()

def save_img(preprocessed_image, cropped_image, fn):
    # Save preprocessed images for debugging
    cv2.imwrite("generated/images/" + fn + "preprocessed_image.png", preprocessed_image)
    cv2.imwrite("generated/images/" + fn + "cropped_image.png", cropped_image)