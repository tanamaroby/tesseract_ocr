import cv2
import numpy as np

import glob
import os

from pprint import pprint as pp
from PIL import Image

class crop: 

    # class attributes
    def __init__(self):
        self.window_name = 'crop'
        self.size_max_image = 2047
        self.debug_mode = False

    # quick cropping methods
    # keep left half
    def crop_left_half(self, image, proportion):

        # Dimensions
        top = 0
        bottom = image.shape[0]
        left = 0
        right = int(image.shape[1] * proportion)

        cropped_img = image[top:bottom, left:right]
        return cropped_img

    # keep bottom half
    def crop_bottom_half(self, image, proportion):
        top = int(image.shape[0] * proportion)
        bot = image.shape[0]
        cropped_img = image[top:bot]
        return cropped_img

    # keep top half
    def crop_top_half(self, image, proportion):
        top = 0
        bot = int(image.shape[0] * (1-proportion))
        cropped_img = image[top:bot]
        return cropped_img

    def get_image_width_height(self, image):
        image_width = image.shape[1]  # current image's width
        image_height = image.shape[0]  # current image's height
        return image_width, image_height


    def calculate_scaled_dimension(self, scale, image):
        # http://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
        image_width, image_height = get_image_width_height(image)
        ratio_of_new_with_to_old = scale / image_width
        dimension = (scale, int(image_height * ratio_of_new_with_to_old))
        return dimension


    def rotate_image(self, image, degree=180):
        # http://www.pyimagesearch.com/2014/01/20/basic-image-manipulations-in-python-and-opencv-resizing-scaling-rotating-and-cropping/
        image_width, image_height = get_image_width_height(image)
        center = (image_width / 2, image_height / 2)
        M = cv2.getRotationMatrix2D(center, degree, 1.0)
        image_rotated = cv2.warpAffine(image, M, (image_width, image_height))
        return image_rotated


    def scale_image(self, image, size):
        image_resized_scaled = cv2.resize(
            image,
            calculate_scaled_dimension(
                size,
                image
            ),
            interpolation=cv2.INTER_AREA
        )
        return image_resized_scaled

    def detect_box(self, image, cropIt=True):
        # https://stackoverflow.com/questions/36982736/how-to-crop-biggest-rectangle-out-of-an-image/36988763
        # Transform colorspace to YUV
        image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        image_y = np.zeros(image_yuv.shape[0:2], np.uint8)
        image_y[:, :] = image_yuv[:, :, 0]

        # Blur to filter high frequency noises
        image_blurred = cv2.GaussianBlur(image_y, (3, 3), 0)
        if (self.debug_mode):  show_image(image_blurred, self.window_name)

        # Apply canny edge-detector
        edges = cv2.Canny(image_blurred, 100, 300, apertureSize=3)
        if (self.debug_mode): show_image(edges, self.window_name)

        # Find extreme outer contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if (self.debug_mode):
            #                                      b  g   r
            cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
            show_image(image, self.window_name)

        # https://stackoverflow.com/questions/37803903/opencv-and-python-for-auto-cropping
        # Remove large countours
        new_contours = []
        for c in contours:
            #if cv2.contourArea(c) < 4000000:
            new_contours.append(c)

        # Get overall bounding box
        best_box = [-1, -1, -1, -1]
        for c in new_contours:
            x, y, w, h = cv2.boundingRect(c)
            if best_box[0] < 0:
                best_box = [x, y, x + w, y + h]
            else:
                if x < best_box[0]:
                    best_box[0] = x
                if y < best_box[1]:
                    best_box[1] = y
                if x + w > best_box[2]:
                    best_box[2] = x + w
                if y + h > best_box[3]:
                    best_box[3] = y + h

        if (self.debug_mode):
            cv2.rectangle(image, (best_box[0], best_box[1]), (best_box[2], best_box[3]), (0, 255, 0), 1)
            show_image(image, self.window_name)

        if (cropIt):
            image = image[best_box[1]:best_box[3], best_box[0]:best_box[2]]
            if (self.debug_mode): show_image(image, self.window_name)

        return image


    def show_image(self, image, window_name):
        # Show image
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, image)
        image_width, image_height = self.get_image_width_height(image)
        #cv2.resizeWindow(window_name, image_width, image_height)

        # Wait before closing
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cut_of_top(image, pixel):
        image_width, image_height = self.get_image_width_height(image)

        # startY, endY, startX, endX coordinates
        new_y = 0+pixel
        image = image[new_y:image_height, 0:image_width]
        return image

    def cut_of_bottom(image, pixel):
        image_width, image_height = self.get_image_width_height(image)

        # startY, endY, startX, endX coordinates
        new_height = image_height-pixel
        image = image[0:new_height, 0:image_width]
        return image


#for file_iterator in glob.iglob(path_in):
#    image = cv2.imread(file_iterator)

#    #image = rotate_image(image, 90)
#    #image = cut_of_bottom(image, 1000)

#    #image = scale_image(image, self.size_max_image)
#    if (self.debug_mode): show_image(image, self.window_name)

#    image = detect_box(image, True)

#    # Create out path
#    if not os.path.exists(path_out):
#        os.makedirs(path_out)

#    # Build output file path
#    file_name_ext = os.path.basename(file_iterator)
#    file_name, file_extension = os.path.splitext(file_name_ext)
#    file_path = os.path.join(path_out, file_name + '.cropped' + file_extension)

#    # Write out file
#    cv2.imwrite(file_path, image)

#    print("Transform file {} to {}".format(
#        file_iterator,
#        file_path
#    ))