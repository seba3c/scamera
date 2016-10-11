import logging

from telegram.ext import Updater, CommandHandler
from telegram.error import TelegramError

from ftpd.models import FTPDServerConfig
from notifications.models import NotificationUserProfile

logger = logging.getLogger(__name__)


class UnregisterdNotificationUserProfile(Exception):
    pass


class UnauthorizedUser(Exception):
    pass


class SCameraBotTelgramHandlers():
    """
    Commands - /setcommands BotFather message
    ping - check availability
    enablesubscription - subscription on
    disablesubscription - subscription off
    register - register to receive bot notifications
    enablenotifications - notifications on
    disablenotifications - notifications off
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

    def _check_user_registered(self, update, check_staff=False):
        logger.debug("Verifying user registered...")
        chat_id = update.message.chat_id
        try:
            nup = NotificationUserProfile.objects.get(telegram_bot_id=chat_id)
            logger.debug("User is registered to operate this bot...")
            if check_staff:
                logger.debug("Checking if user is staff...")
                if nup.user.is_superuser:
                    logger.debug("User is superuser!")
                else:
                    logger.error("User is not superuser!")
                    raise UnauthorizedUser()
            return nup
        except NotificationUserProfile.DoesNotExist:
            logger.error("User is not registered to operate this bot...")
            raise UnregisterdNotificationUserProfile()

    def _handle_user_unregistered(self, bot, update):
        msg = "Sorry! You are not registered to operate this bot."
        self._send_message(bot, update, msg)

    def _handle_user_not_superuser(self, bot, update):
        msg = "Sorry! You don't have permission to use this command."
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

    def _toggle_enabled(self, bot, update, value):
        logger.info("Toggling FTP enabled = %s...", value)
        try:
            self._check_user_registered(update, True)
            ftpd_config = FTPDServerConfig.objects.get()
            ftpd_config.enabled = value
            ftpd_config.save()
            msg = "FTP Notifications %s!" % ("enabled" if value else "disable")
            self._send_message(bot, update, msg)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        except UnauthorizedUser:
            self._handle_user_not_superuser(bot, update)
        except:
            logger.exception()
        logger.info("Subscription disabled!")

    def enable(self, bot, update):
        self._toggle_enabled(bot, update, True)

    def disable(self, bot, update):
        self._toggle_enabled(bot, update, False)

    def _build_updater(self):
        logger.debug("Building telegram bot updater...")
        updater = Updater(self.telegrambot.token)
        updater.dispatcher.add_handler(CommandHandler('ping', self.ping))
        updater.dispatcher.add_handler(CommandHandler('enablesubscription', self.subscribe))
        updater.dispatcher.add_handler(CommandHandler('disablesubscription', self.unsubscribe))
        updater.dispatcher.add_handler(CommandHandler('register', self.register))
        updater.dispatcher.add_handler(CommandHandler('disablenotifications', self.disable))
        updater.dispatcher.add_handler(CommandHandler('enablenotifications', self.enable))
        return updater


def get_telegram_updater(telegrambot):
    handlers = SCameraBotTelgramHandlers(telegrambot)
    return handlers._build_updater()
