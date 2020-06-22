import cv2
import pytesseract
from pytesseract import Output

class imageboxer:
    
    # Main image conversion process
    def box_image(self, image):
        output_data = pytesseract.image_to_data(image, output_type=Output.DICT)
        n_boxes = len(output_data['text'])
        for i in range(n_boxes):
            if int(output_data['conf'][i]) > 60:
                (x, y, w, h) = (output_data['left'][i], output_data['top'][i], output_data['width'][i], output_data['height'][i])
                output_image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return output_image


