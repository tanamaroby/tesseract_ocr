# Guide on how to use the program

**Note:** Currently, the program only supports `.png` format (for id card readers and similar images).

## Getting started

### Installing pytesseract

1. Check that you have pytesseract installed using

		tesseract --version

2. If you don't have pytesseract installed, install it using the command below: 

		pip install pytesseract

## How to use

### Input and output locations

**Note:** There should already be sample files in the input output folder.

1. All the inputs are located in the `documents` folder which should contain either `.jpeg`, `.png`, or `.pdf` files.

2. This program only reads one input at a time and the filename needs to be specified in the main script.

3. All the outputs are located in the `generated` folder which contains both `images` and `text` folder.

4. `images` folder contains both preprocessed and cropped images in `.png` format. 
	These images are only used for debugging to see how the preprocessing and cropping process work. 

5. `text` folder contains both **processed** and **raw** text output extracted from the images. **Processed** text files
	contains formatted text of the extracted data. **Raw** text files are the unformatted text extracted directly from the images. 

6. When the program runs, the main script will read the input specified and generate the image and text files
	into the respective output folders.

### Running the program

1. In `main.py` main script (at the bottom), there should be filepath specified. 

        if __name__ == "__main__":
            # only execute if main script
            parser = argparse.ArgumentParser(description='ocr script for dataset, indicate file name')
            parser.add_argument('--fn', default='documents/PANCard3.jpeg', help='fn of image')
            args = parser.parse_args()
            print(args)
            ocr = OCR(args.fn)
            final_output = ocr.get_text("id")
            print("final", final_output)

2. The filepath is specified in this line: 

        parser.add_argument('--fn', default='documents/PANCard3.jpeg', help='fn of image')

    To change the input, just change the default value. 

3. Run the `main.py` file. The output should now be generated in their respective folders.

### Using the preprocessor

1. This program contains the `imagepreprocessor.py` which contains many preprocessing methods that can be used 
    to improve the image text extraction. 

2. To apply any preprocessing method into the image, just add the function into the `preprocess()` function

        def preprocess(self, image):
            image = self.get_grayscale(image)
            return image

    **Note:** The following should apply grayscaling into the image to turn the image black and white. 

3. To add any preprocessing method, just add it into the function like below.

        def preprocess(self, image):
            image = self.get_grayscale(image)
            image = self.remove_noise(image)
            return image

    **Note:** The following should apply grayscale on the image, and then remove noise from the image. 

### Using the crop

**Note:** Used by `processor.py` to crop the images according to the child classes' specifications.

1. `crop.py` contains useful cropping methods which is used to extract relevant section from the image to make
    output processing a lot easier. 

2. The cropping methods will take in an image as input and return a cropped image according to the functions' specifications. 

### Using the image orientation fixer

**Note:** Currently not called in main script.

1. As of now, `imageorientation.py` only contains image skew detection function where it will take in an image 
    as an input and return the angle of the image in degrees.

### Using the image boxer

**Note:** Currently not called in main script. 

1. `imageboxer.py` is useful for debugging as it creates boxes around text that the pytesseract ocr can read. 

2. Its functions will take in image files and return a boxed image files with boxes around text items depending
    which function is called. 

## Developer Guide

Information on relationship between classes, adding new processor, and how the reader works can be found in the 
[DevGuide.md](DevGuide.md) file. 








