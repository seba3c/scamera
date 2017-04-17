import os
import logging

from imutils import paths

from django.utils import timezone
from django.db import models

from images.app_settings import (images_settings)
from images.processors import ImagePreProcessorFactory

logger = logging.getLogger(__name__)


def settings_asstring():
    ll = list(zip(images_settings.keys(), images_settings.values()))
    lll = list(map(lambda x: "%s: %s" % (x[0], x[1]), ll))
    "\n".join(lll)
    return lll


class PeopleDetectorTest(models.Model):

    state_choices = (('initial', 'initial'),
                     ('running', 'running'),
                     ('finished', 'finished'),
                     ('failed', 'failed'))

    title = models.CharField(max_length=50, default='Test', null=False, blank=False)
    state = models.CharField(choices=state_choices, max_length=10, default='initial',
                             null=False,
                             blank=False)
    settings = models.TextField(default=settings_asstring,
                                null=False,
                                blank=False)

    creation_timestamp = models.DateTimeField("Created",
                                              auto_now_add=True, null=False, blank=False)
    running_timestamp = models.DateTimeField("Executed",
                                             null=True, blank=False)
    time_took = models.FloatField(default=0.0, null=False, blank=True)

    positive_samples_dir = models.CharField(max_length=150, null=True, blank=True)
    negative_samples_dir = models.CharField(max_length=150, null=True, blank=True)
    save_enhaced_images = models.BooleanField(default=False, null=False, blank=False)

    positive_samples_count = models.PositiveIntegerField("Positive Samples",
                                                         null=False, blank=False, default=0)
    negative_samples_count = models.PositiveIntegerField("Negative Samples",
                                                         null=False, blank=False, default=0)

    true_positives = models.PositiveIntegerField("TP", null=False, blank=False, default=0)
    true_negatives = models.PositiveIntegerField("TN", null=False, blank=False, default=0)
    false_positives = models.PositiveIntegerField("FP", null=False, blank=False, default=0)
    false_negatives = models.PositiveIntegerField("FN", null=False, blank=False, default=0)

    _accuracy = models.FloatField(default=0.0, null=False, blank=False)
    _total_samples_count = models.PositiveIntegerField(default=0, null=False, blank=False)

    @classmethod
    def get_test(cls, test_name):
        (obj, created) = cls.objects.get_or_create(title=test_name, state='running')
        if created:
            obj.running_timestamp = timezone.now()
            obj.save()
        return obj

    def run(self):
        self.state = 'running'
        self.running_timestamp = timezone.now()
        self.save()

        output_path = os.path.join(images_settings.image_output_path, "%02d_TEST" % self.pk)
        img_proc = ImagePreProcessorFactory.get_image_preprocessor(self.save_enhaced_images,
                                                                   output_path)

        for im_path in paths.list_images(self.positive_samples_dir):
            result = img_proc.process(im_path)
            if result.count > 0:
                self.inc_TP()
            else:
                self.inc_FP()
            self.time_took += result.time
            self.inc_PS()

        for im_path in paths.list_images(self.negative_samples_dir):
            result = img_proc.process(im_path)
            if result.count <= 0:
                self.inc_TN()
            else:
                self.inc_FN()
            self.time_took += result.time
            self.inc_NS()

        self.finish()

    def finish(self):
        self.state = 'finished'
        self.save()

    def fail(self):
        self.state = 'failed'
        self.save()

    def inc_PS(self):
        self.positive_samples_count += 1

    def inc_NS(self):
        self.negative_samples_count += 1

    def inc_TP(self):
        self.true_positives += 1

    def inc_FN(self):
        self.false_negatives += 1

    def inc_FP(self):
        self.false_positives += 1

    def inc_TN(self):
        self.true_negatives += 1

    @property
    def TP(self):
        return self.true_positives

    @property
    def TN(self):
        return self.true_negatives

    @property
    def FP(self):
        return self.false_positives

    @property
    def FN(self):
        return self.false_negatives

    @property
    def P(self):
        return self.TP + self.FN

    @property
    def N(self):
        return self.FP + self.TN

    @property
    def sensitivity(self):
        """
        sensitivity or true positive rate (TPR)
        """
        try:
            return self.TP / self.P
        except ZeroDivisionError:
            return 0.0

    @property
    def specificity(self):
        """
        specificity (SPC) or True Negative Rate
        """
        try:
            return self.TN / self.N
        except ZeroDivisionError:
            return 0.0

    @property
    def precision(self):
        """
        precision or positive predictive value (PPV)
        """
        try:
            return self.TP / (self.TP + self.FP)
        except ZeroDivisionError:
            return 0.0

    @property
    def negative_predictive_value(self):
        """
        negative predictive value (NPV)
        """
        try:
            return self.TN / (self.TN + self.FN)
        except ZeroDivisionError:
            return 0.0

    @property
    def fall_out(self):
        """
        fall-out or false positive rate (FPR)
        """
        try:
            return self.FP / (self.FP + self.TN)
        except ZeroDivisionError:
            return 0.0

    @property
    def false_discovery_rate(self):
        """
        false discovery rate (FDR)
        """
        return 1 - self.precision

    @property
    def miss_rate(self):
        """
        Miss Rate or False Negative Rate (FNR)
        """
        try:
            return self.FN / (self.FN + self.TP)
        except ZeroDivisionError:
            return 0.0

    @property
    def accuracy(self):
        """
        accuracy (ACC)
        """
        try:
            acc = (self.TP + self.TN) / (self.P + self.N)
        except ZeroDivisionError:
            acc = 0.0

        if acc != self._accuracy:
            self._accuracy = acc
            self.save()
        return acc

    @property
    def balanced_accuracy(self):
        """
        balanced accuracy (BACC)
        """
        try:
            return (self.TP / self.P + self.TN / self.N) / 2
        except ZeroDivisionError:
            return 0.0

    @property
    def total_samples_count(self):
        total = self.positive_samples_count + self.negative_samples_count
        if total != self._total_samples_count:
            self._total_samples_count = total
            self.save()
        return total

    @property
    def avg_time_per_sample(self):
        try:
            return self.time_took / self.total_samples_count
        except ZeroDivisionError:
            return 0.0

    def register_PS_TP(self):
        self.inc_PS()
        self.inc_TP()
        self.save()

    def register_NS_FP(self):
        self.inc_NS()
        self.inc_FP()
        self.save()

    def register_PS_FN(self):
        self.inc_PS()
        self.inc_FN()
        self.save()

    def register_NS_TN(self):
        self.inc_NS()
        self.inc_TN()
        self.save()
