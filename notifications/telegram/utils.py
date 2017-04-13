import telegram


def send_live_test_keyboard(tbot, chat_id):
    keyboard = [[telegram.InlineKeyboardButton("Pos. sample - True pos.",
                                               callback_data='ps-tp')],
                [telegram.InlineKeyboardButton("Neg. sample - False pos.",
                                               callback_data='ns-fp')],
                ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    tbot.sendMessage(chat_id=chat_id,
                     text='This image is:',
                     reply_markup=reply_markup)


def hide_custom_keyboard(tbot, chat_id):
    reply_markup = telegram.ReplyKeyboardHide()
    tbot.sendMessage(chat_id=chat_id, text="Hiding custom keyboard!", reply_markup=reply_markup)
