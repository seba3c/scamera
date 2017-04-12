import logging
import os
import timeit

import cv2

import numpy as np

import imutils
from imutils.object_detection import non_max_suppression

from images.app_settings import images_settings as imsettings


logger = logging.getLogger(__name__)


class ImagePreProcessorResult():

    def __init__(self, path, count=0, time=0):
        self.path = path
        self.count = count
        self.time = time


class ImagePreProcessor(object):

    def __init__(self, save_enhaced_imgs=None, ouput_path=None):
        self.save_enhaced_imgs = save_enhaced_imgs or imsettings.output_enhanced_image
        self.ouput_path = ouput_path or imsettings.image_output_path
        if not os.path.exists(self.ouput_path):
            logger.debug("Creating path '%s'...", self.ouput_path)
            os.makedirs(self.ouput_path, exist_ok=True)

    def process(self, path):
        raise NotImplementedError('Subclasses must implement this method!')


class NullImagePreProcessor(ImagePreProcessor):

    def process(self, path):
        return ImagePreProcessorResult(path)


class HOGPeopleDetectorImagePreProcessor(ImagePreProcessor):

    def __init__(self, save_enhaced_imgs=None, ouput_path=None):

        super(HOGPeopleDetectorImagePreProcessor, self).__init__(save_enhaced_imgs,
                                                                 ouput_path)
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

    def process(self, path):
        logger.info("Analyzing image: '%s'", path)
        new_path = path
        image = cv2.imread(path)  # IMREAD_GRAYSCALE
        image = imutils.resize(image, width=min(self.max_width_size, image.shape[1]))

        start_time = timeit.default_timer()
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
        object_detected_count = len(pick)
        elapsed_time = timeit.default_timer() - start_time

        if object_detected_count > 0:
            # draw the final bounding boxes
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB),
                              self.rect_line_color,
                              self.rect_line_width)

            filename = os.path.basename(path)
            new_path = os.path.join(self.ouput_path, filename)
            cv2.imwrite(new_path, image)

        return ImagePreProcessorResult(new_path, object_detected_count, elapsed_time)


class ImagePreProcessorFactory(object):

    @staticmethod
    def get_image_preprocessor(save_enhaced_imgs=None, ouput_path=None):
        impl = imsettings.implementation
        if impl == 'hog':
            return HOGPeopleDetectorImagePreProcessor(save_enhaced_imgs, ouput_path)
        return NullImagePreProcessor()
