import logging
import dbsettings

logger = logging.getLogger(__name__)


PEOPLE_DETECTOR_IMPL_CHOICES = [('hog', 'Histogram of Oriented Gradients')]


class PeopleDetectorAlgorithmSettingGroup(dbsettings.Group):
    implementation = dbsettings.StringValue(choices=PEOPLE_DETECTOR_IMPL_CHOICES)


class HOGPeopleDetectorSettingGroup(dbsettings.Group):
    min_size = dbsettings.PositiveIntegerValue(required=True, default=400)
    #winStride = (4, 4)
    #padding_tb = 8
    #padding_rl = 8
    scale = dbsettings.FloatValue(required=True, default=1.05)


options = PeopleDetectorAlgorithmSettingGroup('People Detector Algorithm')
options += HOGPeopleDetectorSettingGroup('HOG People Detector')
