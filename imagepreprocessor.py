import cv2

class imagepreprocessor:
    
    # Pre-processing methods
    # Get grayscale images
    def get_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal
    def remove_noise(self, image):
        return cv2.medianBlur(image, 5)

    # Thresholding
    def thresholding(self, image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Dilation
    def dilate(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)

    # Erosion
    def erode(self, image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations = 1)

    # Opening - erosion followed by dilation
    def opening(self, image):
        kernel = np.ones((5,5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel) 

    # Canny edge detection
    def canny(self, image):
        return cv2.Canny(image, 100, 200)

    # Skew correction
    def deskew(self, image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_sCUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    # Template matching
    def match_template(self, image, template):
        return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

    # Pre-process wrapper function (edit accordingly)
    def preprocess(self, image):
        image = self.get_grayscale(image)
        return image