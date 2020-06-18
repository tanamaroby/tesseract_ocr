# Imports
import cv2
import pytesseract
import numpy as np

# Path to image file
img = cv2. imread('images/example_01.png')

# Pre-processing methods
# Get grayscale images
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)

# Thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

# Erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

# Opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel) 

# Canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

# Skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# Pre-process wrapper function (edit accordingly)
def pre_process(image):
    image = get_grayscale(image)
    image = thresholding(image)
    return image

# Show pre-processed image output for debugging
def show_image(image):
    cv2.imshow("Image", image)
    cv2.waitKey(0)

# Process from image to string and print out
preprocessed_image = pre_process(img)
output = pytesseract.image_to_string(preprocessed_image)
print(output)

# Show the pre-processed image
show_image(preprocessed_image)