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
        self.image_preprocessor = imagepreprocessor.imagepreprocessor() # Pre-processor
        self.image_boxer = imageboxer.imageboxer() # Boxer
        self.image_orientation = imageorientation.imageorientation() # Detect orientation
        self.image_cropper = crop.crop() # Cropping tool
        self.output_postprocessor = idprocessor.idprocessor() # Process the output
        self.old_proportion = dict()
        self.old_proportion['left'] = 0.7
        self.new_proportion = dict()
        self.new_proportion['bot'] = 0.25
        self.new_proportion['left'] = 0.7


    def crop_old(self, img):
        # Crop the image
        cropped_image = self.image_cropper.detect_box(img) # image_cropper.crop(img)
        cropped_image = self.image_cropper.crop_left_half(cropped_image, self.old_proportion['left'])
        return cropped_image

    def crop_new(self, img):
        # Crop the image
        cropped_image = self.image_cropper.detect_box(img) # image_cropper.crop(img)
        cropped_image = self.image_cropper.crop_bottom_half(cropped_image, self.new_proportion['bot'])
        cropped_image = self.image_cropper.crop_left_half(cropped_image, self.new_proportion['left'])
        return cropped_image

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
        # Checking if the file given is PDF or Image format
        if ('.pdf' in filepath):
            # In the case of multiple pages
            pages = convert_from_path(filepath)
            image_counter = 1
            for page in pages:
                filename = "page_" + str(image_counter) + ".png"
                page.save('images/' + filename, 'PNG')
                image_counter = image_counter + 1
                file_paths.append('images/' + filename)
        else:
            file_paths.append(filepath)
        return file_paths

    def get_score(self, output):
        fields = ['name', 'dob', 'pan_number']
        score = 0
        for field in fields:
            if field in output and output[field]:
                score += 1
        return score

    def process_id(self):
        outputs = list()
        for file in self.filepath:
            img = cv2.imread(file)
            basename = os.path.basename(file)
            basename = os.path.splitext(basename)[0]

            cropped_image = self.crop_new(img)
            new_output = self.process(cropped_image, basename, "new")
            new_score = self.get_score(new_output)

            cropped_image = self.crop_old(img)
            old_output = self.process(cropped_image, basename, "old")
            old_score = self.get_score(old_output)
            if new_score > old_score:
                output = new_output
            elif new_score == old_score:
                if 'name' in new_output and 'name' in old_output:
                    output = new_output if (new_output['name'] > old_output['name']) else old_output
                else:
                    output = old_output
            else:
                output = old_output
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
    parser.add_argument('--fn', default='documents/PANCard2.jpeg', help='fn of image')
    args = parser.parse_args()
    print(args)
    ocr = OCR(args.fn)
    final_output = ocr.process_id()
    print("final", final_output)
