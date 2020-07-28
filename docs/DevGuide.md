# Developer guide

## Relationship between classes

## Image reader pipeline 

**Note:** Shows what processes the image/document go through step by step. 

1. The image is first read from `documents` folder. 

2. Using the `extract()` method found in corresponding processor child class (such as `idprocessor.py`), the 
    image is cropped out, resulting in an image section that should only contain relevant information. 

3. The image is then processed using `process()` method in `main.py` file where it will undergo preprocessing 
    and have its text extracted out into a string output. 

4. Both cropped and preprocessed images are then saved in the `generated/images` folder. The string output 
    is processed by `postprocess()` method found in corresponding processor child class in order to extract 
    any relevant data.

5. Both raw string output and processed string output are then saved in `generated/text` folder.  

## How to add new processor class

Child processor class are used to extract information with methods tailored to the document type such as ID cards or 
bank statements. 

**Note:** `processor.py` is the parent class which contains basic regex extraction methods.

### Steps

1. Child class should have both `extract()` and `postprocess()` methods. 

2. `extract()` method should have image, name, and callback as parameters (callback should refer to the OCR class
    in `main.py`). 

3. `extract()` method should firstly crop the image (OPTIONAL), then call `process()` method from `main.py`
    which will apply preprocessing on the image and finally extract out text from the image. 

4. `postprocess()` needs to take in raw text output and extract out only relevant information to be returned. 
    `postprocess()` will be called by the `process()` method from `main.py`.

Check out `idprocessor.py` for example on how to create the processor class. 

