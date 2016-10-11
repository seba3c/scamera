import logging

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from solo.models import SingletonModel

from notifications.telegram.models import TelegramNotificationHandler


logger = logging.getLogger(__name__)


class FTPUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # FTPD permissions
    change_directory = models.BooleanField(help_text="e = change directory (CWD, CDUP commands)",
                                           default=True,)
    list_files = models.BooleanField(help_text=
                                     "l = list files (LIST, NLST, STAT, MLSD, MLST, SIZE commands)",
                                     default=True)
    retrieve_file = models.BooleanField(help_text=
                                        "r = retrieve file from the server (RETR command)",
                                        default=True)
    append_data = models.BooleanField(help_text=
                                      "a = append data to an existing file (APPE command)",
                                      default=False)
    delete = models.BooleanField(help_text="d = delete file or directory (DELE, RMD commands)",
                                 default=False)
    rename = models.BooleanField(help_text="f = rename file or directory (RNFR, RNTO commands)",
                                 default=False)
    create_dir = models.BooleanField(help_text="m = create directory (MKD command)",
                                     default=False)
    store = models.BooleanField(help_text="w = store a file to the server (STOR, STOU commands)",
                                default=False)
    change_mode_perm = models.BooleanField(help_text=
                                           "M = change mode/permission (SITE CHMOD command)",
                                           default=False)

    @property
    def homedir(self):
        return slugify(self.user.username)

    @property
    def ftpd_perm(self):
        l = [(self.change_directory, 'e'),
             (self.list_files, 'l'),
             (self.retrieve_file, 'r'),
             (self.append_data, 'a'),
             (self.delete, 'd'),
             (self.rename, 'f'),
             (self.create_dir, 'm'),
             (self.store, 'w'),
             (self.change_mode_perm, 'M')]
        perm = map(lambda x: x[1], filter(lambda x: True if x[0] else False, l))
        return ''.join(perm)

    def __str__(self):
        return "{} - {}".format(self.user, self.ftpd_perm)


class FTPDServerConfig(SingletonModel):

    telegram_notification_handlers = models.ManyToManyField(TelegramNotificationHandler)
    enabled = models.BooleanField(default=True,
                                  help_text="Start/Stop accepting new FTP connections")

    def get_notification_handlers(self, only_enabled=False):
        handlers = []
        if only_enabled:
            handlers.extend(self.telegram_notification_handlers.filter(enabled=True))
        return handlers

    def get_enabled_notification_handlers(self):
        return self.get_notification_handlers(only_enabled=True)

    def get_notification_handlers_count(self):
        count = self.telegram_notification_handlers.count()
        return count

    def __str__(self):
        return "Notification Handlers: %d - Enabled: %s" % (self.get_notification_handlers_count(),
                                                            self.enabled)
