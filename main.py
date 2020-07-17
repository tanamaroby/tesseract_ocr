# Library imports
import os
import argparse
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

filepath = 'documents/PANCard3.jpeg'

class OCR:
    def __init__(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Converting PDF to PNG when necessary
        self.filepath = self.get_paths(path)

        # Initiating all the tools
        self.image_preprocessor = imagepreprocessor.imagepreprocessor() # Pre-processor
        self.image_boxer = imageboxer.imageboxer() # Boxer
        self.image_orientation = imageorientation.imageorientation() # Detect orientation
        self.image_cropper = crop.crop() # Cropping tool
        self.output_postprocessor = idprocessor.idprocessor() # Process the output


    def process(self, cropped_image, basename, type):
        # Process from image to string
        preprocessed_image = self.image_preprocessor.preprocess(cropped_image)
        output = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6')

        # Processing the output
        processedoutput, processed_id = self.output_postprocessor.postprocess(output)
        self.save_output(output, processedoutput, basename + type)
        self.save_img(preprocessed_image, cropped_image, basename + type)
        return processed_id

    def get_paths(self, filepath):
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



    def process_id(self):
        outputs = list()
        for file in self.filepath:
            img = cv2.imread(file)
            basename = os.path.basename(file)
            basename = os.path.splitext(basename)[0]
            output = self.output_postprocessor.extract(img, basename, self)
            outputs.append(output)
        return outputs

    def save_output(self, output, processed_output, fn):
        # Writing into file for documentation
        with open('generated/text/' + fn + 'rawoutput.txt', 'w+') as file:
            file.write(output)
            file.close()
        # Writing processed output
        with open('generated/text/' + fn + 'processedoutput.txt', 'w+') as file:
            file.write(processed_output)
            file.close()

    def save_img(self, preprocessed_image, cropped_image, fn):
        # Save preprocessed images for debugging
        cv2.imwrite("generated/images/" + fn + "preprocessed_image.png", preprocessed_image)
        cv2.imwrite("generated/images/" + fn + "cropped_image.png", cropped_image)

if __name__ == "__main__":
    # only execute if main script
    parser = argparse.ArgumentParser(description='ocr script for dataset, indicate file name')
    parser.add_argument('--fn', default='documents/PANCard3.jpeg', help='fn of image')
    args = parser.parse_args()
    print(args)
    ocr = OCR(args.fn)
    final_output = ocr.process_id()
    print("final", final_output)
