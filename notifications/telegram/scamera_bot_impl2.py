import logging

from telegram.ext.callbackqueryhandler import CallbackQueryHandler

from notifications.telegram.scamera_bot_base import (SCameraBotTelegramHandlers,
                                                     UnregisterdNotificationUserProfile)
from images.models import PeopleDetectorTest


logger = logging.getLogger(__name__)


class SCameraBotTelegramHandlers2(SCameraBotTelegramHandlers):
    """
    Commands - /setcommands BotFather message
    ping - check availability
    status - current notification status
    register - start to receive notifications
    subscribe - subscription on
    unsubscribe - subscription off
    activate - notifications on
    deactivate - notifications off
    """

    def handle_callback(self, bot, update):
        logger.info("Handling callback...")
        try:
            self._check_user_registered(update)
            query = update.callback_query
            logger.debug("Callback query: %s", query)

            test = PeopleDetectorTest.get_live_test()
            if query.data == 'ps-tp':
                test.inc_PS()
                test.inc_TP()
                test.save()
                text = "Selected option: %s" % query.data
            elif query.data == 'ns-fp':
                test.inc_NS()
                test.inc_FP()
                test.save()
                text = "Selected option: %s" % query.data
            else:
                text = "Invalid callback data!"
                logger.warning("Invalid callback data!")

            bot.editMessageText(text=text,
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Callback handled!")

    def _build_updater(self):
        updater = super(SCameraBotTelegramHandlers2, self)._build_updater()
        updater.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))
        return updater


def get_telegram_updater(telegrambot):
    handlers = SCameraBotTelegramHandlers2(telegrambot)
    return handlers._build_updater()
