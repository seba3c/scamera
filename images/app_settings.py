import logging
import dbsettings

logger = logging.getLogger(__name__)


class HOGPeopleDetectorSettingGroup(dbsettings.Group):
    image_max_width_size = dbsettings.PositiveIntegerValue(help_text='Image maximum width (reduces detection time and improves overall accuracy)',
                                                           required=True, default=400)

    win_stride_x = dbsettings.PositiveIntegerValue(help_text='“step size” in X of the sliding window',
                                                   required=True, default=4)
    win_stride_y = dbsettings.PositiveIntegerValue(help_text='“step size” in Y of the sliding window',
                                                   required=True, default=4)

    scale = dbsettings.FloatValue(help_text="controls the factor in which our image is resized at each layer of the image pyramid",
                                  required=True, default=1.05,
                                  )

    padding_x = dbsettings.PositiveIntegerValue(help_text='the number of pixels in X direction in which the sliding window ROI is “padded” prior to HOG feature extraction',
                                                required=True, default=4)
    padding_y = dbsettings.PositiveIntegerValue(help_text='the number of pixels in Y direction in which the sliding window ROI is “padded” prior to HOG feature extraction',
                                                required=True, default=4)

    non_maxima_suppression_thresh = dbsettings.FloatValue(description='Non maxima suppression threshold',
                                                          help_text='suppress bounding boxes that overlap with a specified threshold',
                                                          required=True,
                                                          default=0.65)


PEOPLE_DETECTOR_IMPL_CHOICES = [(None, '-'),
                                ('hog', 'Histogram of Oriented Gradients')]


class RGBValue(dbsettings.MultiSeparatorValue):

    def to_python(self, value):
        val = dbsettings.MultiSeparatorValue.to_python(self, value)
        val = [0, 0, 0] if val is None else val + [0, 0, 0]
        val = val[:3]
        return (int(val[0]), int(val[1]), int(val[2]))


class PeopleDetectorAlgorithmSettingGroup(dbsettings.Group):

    implementation = dbsettings.StringValue(description='People image tracking algorithm implementation',
                                            required=False,
                                            default='hog',
                                            choices=PEOPLE_DETECTOR_IMPL_CHOICES)

    rect_line_width = dbsettings.PositiveIntegerValue(description='People tracking rectangle line width (px)',
                                                      required=True, default=2)

    rect_line_color = RGBValue(description='People tracking rectangle color (RGB)',
                               required=True, default=['0', '0', '255'],
                               separator=',')

    output_enhanced_image = dbsettings.BooleanValue(description='Save image enhanced with people tracking data',
                                                    required=True, default=True)

    image_output_path = dbsettings.StringValue(help_text='Output path for image enhanced with people tracking data',
                                               required=True,
                                               default='/tmp/scamera/people_tracking/')


images_settings = PeopleDetectorAlgorithmSettingGroup('People Detector Algorithm')
images_settings += HOGPeopleDetectorSettingGroup('HOG People Detector')
