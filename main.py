# Library imports
import os
import argparse
import cv2
import pytesseract
import numpy as np


# Self-defined classes imports
import imagepreprocessor
import imageboxer
import imageorientation
import idprocessor
import crop
import utility
import processor

filepath = 'documents/PANCard3.jpeg'

class OCR:
    def __init__(self, path):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # Converting PDF to PNG when necessary
        self.filepath = utility.get_paths(path)

        # Initiating all the tools
        self.image_preprocessor = imagepreprocessor.imagepreprocessor() # Pre-processor
        self.image_boxer = imageboxer.imageboxer() # Boxer
        self.image_orientation = imageorientation.imageorientation() # Detect orientation
        self.image_cropper = crop.crop() # Cropping tool
        self.id_postprocessor = idprocessor.idprocessor() # Process the output
        self.output_postprocessor = processor.processor()


    def process(self, cropped_image, basename, type):
        # Process from image to string
        preprocessed_image = self.image_preprocessor.preprocess(cropped_image)
        output = pytesseract.image_to_string(preprocessed_image, lang='eng', config='--psm 6')

        # Processing the output
        processedoutput, processed_id = self.output_postprocessor.postprocess(output)
        utility.save_output(output, processedoutput, basename + type)
        utility.save_img(preprocessed_image, cropped_image, basename + type)
        return processed_id

    def get_handler(self, type):
        if type == "id":
            self.output_postprocessor = self.id_postprocessor
        return


    def get_text(self, type):
        self.get_handler(type)
        outputs = list()
        for file in self.filepath:
            img = cv2.imread(file)
            basename = os.path.basename(file)
            basename = os.path.splitext(basename)[0]
            output = self.output_postprocessor.extract(img, basename, self)
            outputs.append(output)
        return outputs



if __name__ == "__main__":
    # only execute if main script
    parser = argparse.ArgumentParser(description='ocr script for dataset, indicate file name')
    parser.add_argument('--fn', default='documents/PANCard3.jpeg', help='fn of image')
    args = parser.parse_args()
    print(args)
    ocr = OCR(args.fn)
    final_output = ocr.get_text("id")
    print("final", final_output)
