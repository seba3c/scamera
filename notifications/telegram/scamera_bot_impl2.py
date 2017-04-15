import logging

from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler

from images.models import PeopleDetectorTest

from notifications.telegram.scamera_bot_base import (SCameraBotTelegramHandlers,
                                                     UnregisterdNotificationUserProfile)
from notifications.telegram.utils import (POS_SAMPLE_TRUE_POS, NEG_SAMPLE_FALSE_POS)


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
            if query.data in [POS_SAMPLE_TRUE_POS,
                              NEG_SAMPLE_FALSE_POS]:
                test = PeopleDetectorTest.get_test(self.telegrambot.name)
                if query.data == POS_SAMPLE_TRUE_POS:
                    test.register_PS_TP()
                    text = "Image registered as 'Positive Sample - True Positive'"
                elif query.data == NEG_SAMPLE_FALSE_POS:
                    test.register_NS_FP()
                    text = "Image registered as 'Negative Sample - False Positive'"
            else:
                text = "Invalid callback data!"
                logger.error("Invalid callback data '%s'!", query)

            bot.editMessageText(text=text,
                                chat_id=query.message.chat_id,
                                message_id=query.message.message_id)
        except UnregisterdNotificationUserProfile:
            self._handle_user_unregistered(bot, update)
        logger.info("Callback handled!")

    def status(self, bot, update):
        super(SCameraBotTelegramHandlers2, self).status(bot, update)
        tbot = self.telegrambot
        if tbot.debug:
            test = PeopleDetectorTest.get_test(self.telegrambot.name)
            msg = "Live Test enabled\n"
            msg += "Accuracy: %.2f\n" % test.accuracy
            msg += "Total positive samples: %d\n" % test.positive_samples_count
            msg += "Total negative samples: %d\n" % test.negative_samples_count
            msg += "True positives (TP): %d\n" % test.TP
            msg += "False positives (FP): %d\n" % test.FP
            self._send_message(bot, update, msg)

    def _build_updater(self):
        updater = super(SCameraBotTelegramHandlers2, self)._build_updater()
        updater.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))
        updater.dispatcher.add_handler(CommandHandler('status', self.status))
        return updater


def get_telegram_updater(telegrambot):
    handlers = SCameraBotTelegramHandlers2(telegrambot)
    return handlers._build_updater()
