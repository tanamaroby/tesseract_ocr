import re

class idprocessor: 

    # Checks if a string has numbers
    def hasnumbers(self, input):
        return bool(re.search(r'/d', input))

    # Checking for names
    # Checking for all UPPER CASE words and obtaining name by process of elimination
    def namevalidator(self, input):
        inputlines = input.splitlines()

        # Go through the input line by line
        for line in inputlines:

            # Only concerns upper case lines
            if line.isupper():

                # Ensuring that it is not PAN Number
                if not self.hasnumbers(line):

                    # Removing common keyword for the PAN Card titles
                    bannedwords = ["INCOME", "TAX", "DEPARTMENT", "GOVT", "OF", "INDIA"]
                    if not any(word in line for word in bannedwords):
                        return line

        return "Name not found!"

    # Checking output for PANNumber, returns the number if found
    def pannumbervalidator(self, input):
        regexmatch = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]', input)
        if regexmatch is not None:
            return regexmatch.group()
        else:
            return "PAN not found!"

    # Checking output for Date of Birth, returns the number if found
    def datevalidator(self, input):
        regexmatch = re.search(r'\d{2}[-/]\d{2}[-/]\d{4}', input)
        if regexmatch is not None:
            return regexmatch.group()
        else: 
            return "Date of birth not found!"

    def postprocess(self, input):
        name = self.namevalidator(input)
        pannumber = self.pannumbervalidator(input)
        dateofbirth = self.datevalidator(input)
        
        output = "Your name is: " + name + "\n\n"
        output += "Your PAN Number is: " + pannumber + "\n\n"
        output += "Your date of birth is: " + dateofbirth
        return output