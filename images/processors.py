import logging
import os

import cv2
from cv2 import IMREAD_GRAYSCALE

import numpy as np

import imutils
from imutils.object_detection import non_max_suppression

from images.app_settings import images_settings as imsettings


logger = logging.getLogger(__name__)


class ImagePreProcessor(object):

    def process(self, path):
        raise NotImplementedError('Subclasses must implement this method!')


class NullImagePreProcessor(ImagePreProcessor):

    def process(self, path):
        return path


class HOGPeopleDetectorImagePreProcessor(ImagePreProcessor):

    def __init__(self):
        # initialize the HOG descriptor/person detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.max_width_size = imsettings.image_max_width_size

        self.winStride = (imsettings.win_stride_x, imsettings.win_stride_y)
        self.padding = (imsettings.padding_x, imsettings.padding_y)
        self.scale = imsettings.scale

        self.rect_line_color = imsettings.rect_line_color
        self.rect_line_width = imsettings.rect_line_width

        self.overlapThresh = imsettings.non_maxima_suppression_thresh

        self.ouput_path = imsettings.image_output_path
        if not os.path.exists(self.ouput_path):
            logger.debug("Creating path '%s'...", self.ouput_path)
            os.makedirs(self.ouput_path, exist_ok=True)

    def process(self, path):
        logger.info("Analyzing image: '%s'", path)
        new_path = path
        image = cv2.imread(path)  # IMREAD_GRAYSCALE
        image = imutils.resize(image, width=min(self.max_width_size, image.shape[1]))

        # detect people in the image
        (rects, weights) = self.hog.detectMultiScale(image,
                                                     winStride=self.winStride,
                                                     padding=self.padding,
                                                     scale=self.scale)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=self.overlapThresh)

        if len(pick) > 0:
            # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB),
                              self.rect_line_color,
                              self.rect_line_width)

            filename = os.path.basename(path)
            new_path = os.path.join(self.ouput_path, filename)
            cv2.imwrite(new_path, image)

        return new_path


class ImagePreProcessorFactory(object):

    @staticmethod
    def get_image_preprocessor():
        impl = imsettings.implementation
        if impl == 'hog':
            return HOGPeopleDetectorImagePreProcessor()
        return NullImagePreProcessor()
