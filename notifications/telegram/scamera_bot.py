import logging

from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError
from notifications.models import NotificationUserProfile

logger = logging.getLogger(__name__)


class UnregisterdNotificationUserProfile(Exception):
    pass


class SCameraBotTelgramHandlers():
    """
    Commands - /setcommands BotFather message
    ping - check availability
    enablesubscription - enable bot notifications
    disablesubscription - disable bot notifications
    register - register to receive bot notifications
    """

    def __init__(self, telegrambot):
        logger.debug("Initializing telegram bot handlers...")
        self.telegrambot = telegrambot

    def _send_message(self, bot, update, msg):
        try:
            chat_id = update.message.chat_id
            logger.debug("chat_id: %s", chat_id)
            bot.sendMessage(chat_id=chat_id, text=msg)
        except TelegramError:
            logger.error("Error sending message! chat_id: %s")

    def _check_user_registered(self, update):
        logger.debug("Verifying user registered...")
        chat_id = update.message.chat_id
        try:
            nup = NotificationUserProfile.objects.get(telegram_bot_id=chat_id)
            logger.debug("User is registered to operate this bot...")
            return nup
        except NotificationUserProfile.DoesNotExist:
            logger.error("User is not registered to operate this bot...")
            raise UnregisterdNotificationUserProfile()

    def _handle_user_unregistered(self, bot, update):
        msg = "Sorry! You are not registered to operate this bot."
        self._send_message(bot, update, msg)

    def ping(self, bot, update):
        logger.info("Pinging...")
        try:
            self._check_user_registered(update)
            me = bot.getMe()
            logger.debug(me)
            msg = "botname: @%s\nid: %s" % (me['username'], me['id'])
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Ping OK!")

    def subscribe(self, bot, update):
        logger.info("Enabling subscription...")
        try:
            nup = self._check_user_registered(update)
            self.telegrambot.subscribe(nup)
            msg = "Successfully subscribed!"
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Subscription enabled!")

    def unsubscribe(self, bot, update):
        logger.info("Disabling subscription...")
        try:
            nup = self._check_user_registered(update)
            self.telegrambot.unsubscribe(nup)
            msg = "Successfully unsubscribed!"
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except:
            logger.exception()
        logger.info("Subscription disabled!")

    def register(self, bot, update):
        msg = "Sorry! At this moment this option is unavailable."
        self._send_message(bot, update, msg)


def start_telegram_bot(telegrambot):
    logger.debug("Initializing telegram bot...")
    updater = Updater(telegrambot.token)

    handlers = SCameraBotTelgramHandlers(telegrambot)

    updater.dispatcher.add_handler(CommandHandler('ping', handlers.ping))
    updater.dispatcher.add_handler(CommandHandler('enablesubscription', handlers.subscribe))
    updater.dispatcher.add_handler(CommandHandler('disablesubscription', handlers.unsubscribe))
    updater.dispatcher.add_handler(CommandHandler('register', handlers.register))

    updater.start_polling()
    logger.debug("Telegram bot %s running...", telegrambot)
    updater.idle()


def run(telegrambot):
    logger.info("Running telegram bot %s", telegrambot.name)
    start_telegram_bot(telegrambot)
