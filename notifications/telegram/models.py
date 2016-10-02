import logging
import telegram

from django.db import models
from telegram.error import TelegramError

from notifications.models import NotificationHandler


logger = logging.getLogger(__name__)


class TelegramBot(models.Model):

    name = models.CharField(max_length=20, null=False, primary_key=True)
    token = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return "@%s" % self.name

    def _get_telegram_bot(self):
        return telegram.Bot(token=self.token)

    def subscribe(self, nup):
        self.telegramnotificationhandler.subscribe(nup)

    def unsubscribe(self, nup):
        self.telegramnotificationhandler.unsubscribe(nup)


class TelegramNotificationHandler(NotificationHandler):

    telegram_bot = models.OneToOneField(TelegramBot, on_delete=models.CASCADE)

    def _handle_new_notification(self, file=None):
        logger.debug("New notification received, sending data to telegram subscribers...")

        tbot = self._get_telegram_bot()
        msg = "Motion detected!"
        file_id = None
        for s in self.subscribers.all():
            logger.info("Sending notification to %s", s)
            try:
                logger.debug("Sending telegram message...")
                tbot.sendMessage(chat_id=s.telegram_bot_id, text=msg)
                if file_id:
                    logger.debug("Sending telegram photo (existing server photo)...")
                    tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file_id)
                elif file:
                    logger.debug("Sending telegram photo (new photo)...")
                    tmsg = tbot.sendPhoto(chat_id=s.telegram_bot_id, photo=file)
                    file_id = tmsg.photo[0].file_id
            except TelegramError:
                logger.error("Message could not be sent to chat id: %s", s.telegram_bot_id)

    def __str__(self):
        return "%s [%s] | subscribers: %d" % (self.name, self.telegram_bot,
                                              self.subscribers.all().count())

    def _get_telegram_bot(self):
        return self.telegram_bot._get_telegram_bot()
