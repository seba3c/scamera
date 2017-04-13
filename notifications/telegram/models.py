import logging
import telegram

from telegram.error import TelegramError
from notifications.telegram import utils

from django.db import models
from django.core.exceptions import PermissionDenied

from images.app_settings import (images_settings)
from notifications.models import NotificationHandler


logger = logging.getLogger(__name__)


class TelegramBot(models.Model):

    name = models.CharField(max_length=25, null=False, primary_key=True)
    # allows more than one telegram bot implementation with the same token
    token = models.CharField(max_length=100, null=False, unique=True)

    module_name = models.CharField(max_length=25, null=True)

    def __str__(self):
        return "@%s" % self.name

    def _get_telegram_bot(self):
        return telegram.Bot(token=self.token)

    def subscribe(self, nup):
        self.telegramnotificationhandler.subscribe(nup)

    def unsubscribe(self, nup):
        self.telegramnotificationhandler.unsubscribe(nup)

    def is_active(self):
        return self.telegramnotificationhandler.ftp_user.user.is_active

    def is_subscribed(self, nup):
        return self.telegramnotificationhandler.subscribers.filter(id=nup.id).exists()

    def toggle_activate(self, nup, value):
        if not nup.user.is_superuser:
            raise PermissionDenied()
        ftp_user = self.telegramnotificationhandler.ftp_user
        logger.debug("Changing is_active = %s... %s", value, ftp_user.user)
        ftp_user.user.is_active = value
        logger.debug("Saving associated user...")
        ftp_user.user.save()
        logger.debug("User saved!")

    def activate(self, nup):
        self.toggle_activate(nup, True)

    def deactivate(self, nup):
        self.toggle_activate(nup, False)

    def send_notification(self, path=None, obj_count=0):
        self.telegramnotificationhandler._handle_new_notification(path, obj_count)

    def hide_custom_keyboard(self):
        self.telegramnotificationhandler._hide_custom_keyboard()


class TelegramNotificationHandler(NotificationHandler):

    telegram_bot = models.OneToOneField(TelegramBot, on_delete=models.CASCADE)

    def _handle_new_notification(self, path=None, object_count=0):
        logger.debug("New notification received, sending data to telegram subscribers...")

        if path:
            file = open(path,'rb')
        else:
            file = None

        tbot = self._get_telegram_bot()
        file_id = None
        for s in self.subscribers.all():
            logger.info("Sending notification to %s", s)
            try:
                logger.debug("Sending telegram message...")
                self._send_message(tbot, s.telegram_bot_id, object_count)
                self._send_photo(tbot, s.telegram_bot_id, file, file_id)
            except TelegramError:
                logger.error("Message could not be sent to chat id: %s", s.telegram_bot_id)

    def _hide_custom_keyboard(self):
        tbot = self._get_telegram_bot()
        for s in self.subscribers.all():
            utils.hide_custom_keyboard(tbot, s.telegram_bot_id)

    def _send_photo(self, tbot, chat_id, file=None, file_id=None):
        new_file_id = None
        if file_id or file:
            if file_id:
                logger.debug("Sending telegram photo (existing server photo)...")
                tbot.sendPhoto(chat_id=chat_id, photo=file_id)
                new_file_id = file_id
            else:
                logger.debug("Sending telegram photo (new photo)...")
                tmsg = tbot.sendPhoto(chat_id=chat_id, photo=file)
                new_file_id = tmsg.photo[0].file_id

            if images_settings.enable_telegrambot_live_test:
                logger.debug("Telegram live test enabled! Sending keyboard to evaluate last notification...")
                utils.send_live_test_keyboard(tbot, chat_id)

        return new_file_id

    def _send_message(self, tbot, chat_id, object_count=0):
        parse_mode = telegram.ParseMode.HTML
        template = "<b style='color:{color}'>{msg}</b>"
        if object_count > 0:
            i = 3
            msg = template.format(color='red', msg='ALERT: Motion Detected!')
        else:
            i = 1
            msg = template.format(color='yellow', msg='WARNING: Motion Detected!')
        for _ in range(i):
            tbot.sendMessage(chat_id=chat_id, text=msg, parse_mode=parse_mode)

    def __str__(self):
        return "%s [%s] | subscribers: %d" % (self.name, self.telegram_bot,
                                              self.subscribers.count())

    def _get_telegram_bot(self):
        return self.telegram_bot._get_telegram_bot()
