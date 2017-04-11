import logging
import telegram

from django.db import models
from telegram.error import TelegramError

from notifications.models import NotificationHandler
from django.core.exceptions import PermissionDenied


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


class TelegramNotificationHandler(NotificationHandler):

    telegram_bot = models.OneToOneField(TelegramBot, on_delete=models.CASCADE)

    def _handle_new_notification(self, path=None, object_count=0):
        logger.debug("New notification received, sending data to telegram subscribers...")

        file = open(path,'rb')

        tbot = self._get_telegram_bot()
        file_id = None
        for s in self.subscribers.all():
            logger.info("Sending notification to %s", s)
            try:
                logger.debug("Sending telegram message...")
                self._send_message(tbot, s.telegram_bot_id, object_count)
                if file_id:
                    logger.debug("Sending telegram photo (existing server photo)...")
                    tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file_id)
                elif file:
                    logger.debug("Sending telegram photo (new photo)...")
                    tmsg = tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file)
                    file_id = tmsg.photo[0].file_id
            except TelegramError:
                logger.error("Message could not be sent to chat id: %s", s.telegram_bot_id)

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
