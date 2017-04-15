import telegram

POS_SAMPLE_TRUE_POS = 'ps-tp'
NEG_SAMPLE_FALSE_POS = 'ns-fp'


def send_live_test_keyboard(tbot, chat_id):
    keyboard = [[telegram.InlineKeyboardButton("pos-sample/true-pos",
                                               callback_data=POS_SAMPLE_TRUE_POS)],
                [telegram.InlineKeyboardButton("neg-sample/false-pos",
                                               callback_data=NEG_SAMPLE_FALSE_POS)],
                ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    tbot.sendMessage(chat_id=chat_id,
                     text='Debug is enabled. This image is:',
                     reply_markup=reply_markup)


def hide_custom_keyboard(tbot, chat_id):
    reply_markup = telegram.ReplyKeyboardHide()
    tbot.sendMessage(chat_id=chat_id, text="Hiding custom keyboard!", reply_markup=reply_markup)
