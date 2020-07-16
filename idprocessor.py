import re

class idprocessor: 

    # Checks if a string has numbers
    def hasnumbers(self, input):
        return bool(re.search(r'\d', input))

    # Checking for names
    # Checking for all UPPER CASE words and obtaining name by process of elimination
    def namevalidator(self, input):
        # Ensuring that it is not PAN Number
        if not self.hasnumbers(input):
            return input
        return False

    # Checking output for PANNumber, returns the number if found
    def pannumbervalidator(self, input):
        regexmatch = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', input)
        if regexmatch is not None:
            return regexmatch.group()
        else:
            return False

    # Checking output for Date of Birth, returns the number if found
    def datevalidator(self, input):
        regexmatch = re.search(r'\d{2}[-/]\d{2}[-/]\d{4}', input)
        if regexmatch is not None:
            return regexmatch.group()
        else: 
            return False

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