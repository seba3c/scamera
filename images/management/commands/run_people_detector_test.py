import logging

from django.core.management.base import BaseCommand
from images.models import PeopleDetectorTest


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the current people detector algorithm implementation with current settings'

    def add_arguments(self, parser):
        parser.add_argument('negative_dir',
                            type=str,
                            help="Input directory with negative samples",
                            nargs=1,
                            )
        parser.add_argument('positive_dir',
                            type=str,
                            help="Input directory with positive samples",
                            nargs=1,
                            )

    def handle(self, *args, **options):
        logger.info("Running test command...")

        negative_dir_samples = options['negative_dir'].pop()
        positive_dir_samples = options['positive_dir'].pop()

        logger.debug("Negative samples dir: %s", negative_dir_samples)
        logger.debug("Positive samples dir: %s", positive_dir_samples)

        test = PeopleDetectorTest.objects.create(positive_samples_dir=positive_dir_samples,
                                                 negative_samples_dir=negative_dir_samples,
                                                 save_enhaced_images=True)

        test.run()

        logger.info("Test finished! Bye!")
