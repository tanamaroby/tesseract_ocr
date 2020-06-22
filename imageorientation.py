import re
import pytesseract

class imageorientation:

    def detect_angle(self, image):
        osd = pytesseract.image_to_osd(image)
        angle = re.search('(?<=Rotate: )\d+', osd).group(0)
        print("Angle of document: " + angle + " degrees.")



            