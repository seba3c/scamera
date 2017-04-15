from notifications.telegram.scamera_bot_base import SCameraBotTelegramHandlers


def get_telegram_updater(telegrambot):
    handlers = SCameraBotTelegramHandlers(telegrambot)
    return handlers._build_updater()
