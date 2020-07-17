import re
import processor

class idprocessor(processor.processor):

    def __init__(self):
        super().__init__()
        # Cut proportion for old version of the PANCard
        self.old_proportion = dict()
        self.old_proportion['left'] = 0.7

        # Cut proportion for new version of the PANCard
        self.new_proportion = dict()
        self.new_proportion['bot'] = 0.25
        self.new_proportion['left'] = 0.7


    def get_score(self, output):
        # Confidence score of the reading
        fields = ['name', 'dob', 'pan_number']
        score = 0
        for field in fields:
            if field in output and output[field]:
                score += 1
        return score

    def crop_old(self, img):
        # Crop the image according to the old PANCard proportion specified
        cropped_image = self.image_cropper.detect_box(img) # image_cropper.crop(img)
        cropped_image = self.image_cropper.crop_left_half(cropped_image, self.old_proportion['left'])
        return cropped_image

    def crop_new(self, img):
        # Crop the image according to the new PANCard proportion specified
        cropped_image = self.image_cropper.detect_box(img) # image_cropper.crop(img)
        cropped_image = self.image_cropper.crop_bottom_half(cropped_image, self.new_proportion['bot'])
        cropped_image = self.image_cropper.crop_left_half(cropped_image, self.new_proportion['left'])
        return cropped_image

    def extract(self, img, basename, callback):
        # Process the output for both old and new PANCard versions
        cropped_image = self.crop_new(img)
        new_output = callback.process(cropped_image, basename, "new")
        new_score = self.get_score(new_output)

        cropped_image = self.crop_old(img)
        old_output = callback.process(cropped_image, basename, "old")
        old_score = self.get_score(old_output)

        # Comparing confidence score for both processes to determine the PANCard version
        output = old_output
        if new_score > old_score:
            output = new_output
        elif new_score == old_score:
            if 'name' in new_output and 'name' in old_output:
                output = new_output if (len(new_output['name']) > len(old_output['name'])) else old_output
            else:
                output = old_output
        return output

    def postprocess(self, input):
        processed_id = dict()
        name = False
        pan_number = False
        dob = False
        inputlines = input.splitlines()
        # Go through the input line by line
        for line in inputlines:
            # Only concerns upper case lines
            if not pan_number and self.hasnumbers(line):
                pan_number = self.pannumbervalidator(line)
                processed_id['pan_number'] = pan_number
            if line.isupper():
                # Removing common keyword for the PAN Card titles
                bannedwords = ["INCOME", "TAX", "DEPARTMENT", "GOVT", "OF", "INDIA", "Permanent", "Account", "Number"]
                if not any(word in line for word in bannedwords):
                    if not name:
                        name = self.namevalidator(line)
                        processed_id['name'] = name
            elif not dob and self.hasnumbers(line):
                dob = self.datevalidator(line)
                processed_id['dob'] = dob

        output = "Your name is: " + (name if name else "Not Found") + "\n\n"
        output += "Your PAN Number is: " + (pan_number if pan_number else "Not Found") + "\n\n"
        output += "Your date of birth is: " + (dob if dob else "Not Found")
        print(processed_id)
        return output, processed_id