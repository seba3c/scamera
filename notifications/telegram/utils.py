import telegram

POS_SAMPLE_TRUE_POS = 'ps-tp'
NEG_SAMPLE_FALSE_POS = 'ns-fp'
POS_SAMPLE_FALSE_NEG = 'ps-fn'
NEG_SAMPLE_TRUE_NEG = 'ns-tn'
DISCARD_SAMPLE = 'discard'


def send_live_test_keyboard(tbot, chat_id):
    keyboard = [[telegram.InlineKeyboardButton(POS_SAMPLE_TRUE_POS.upper(),
                                               callback_data=POS_SAMPLE_TRUE_POS),
                 telegram.InlineKeyboardButton(NEG_SAMPLE_FALSE_POS.upper(),
                                               callback_data=NEG_SAMPLE_FALSE_POS)],
                [telegram.InlineKeyboardButton(POS_SAMPLE_FALSE_NEG.upper(),
                                               callback_data=POS_SAMPLE_FALSE_NEG),
                 telegram.InlineKeyboardButton(NEG_SAMPLE_TRUE_NEG.upper(),
                                               callback_data=NEG_SAMPLE_TRUE_NEG)],
                [telegram.InlineKeyboardButton(DISCARD_SAMPLE.upper(),
                                               callback_data=DISCARD_SAMPLE)],
                ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    tbot.sendMessage(chat_id=chat_id,
                     text='Debug is enabled. This image is:',
                     reply_markup=reply_markup)


def hide_custom_keyboard(tbot, chat_id):
    reply_markup = telegram.ReplyKeyboardHide()
    tbot.sendMessage(chat_id=chat_id, text="Hiding custom keyboard!", reply_markup=reply_markup)
