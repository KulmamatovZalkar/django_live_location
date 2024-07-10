import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = '7471557412:AAFVvom3aSU4GnFJg7L6fxhLheOO-ZOv97g'

updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Please share your live location manually using the Telegram app.')


def location(update: Update, context: CallbackContext):
    message = update.edited_message if update.edited_message else update.message
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude

        # Send the location to Django via channels
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'location_group',
            {
                'type': 'location_message',
                'latitude': latitude,
                'longitude': longitude
            }
        )
    else:
        logger.warning("Received message with no location")


def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


start_handler = CommandHandler('start', start)
location_handler = MessageHandler(Filters.location, location)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(location_handler)
dispatcher.add_error_handler(error)


def run_bot():
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
