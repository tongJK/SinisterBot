import json
import requests
import time
import urllib
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = 'Your Token'
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:

        user_name = str(updates['result'][0]['message']['from']['first_name']).capitalize()
        text = 'Hi {} I\'m SinisBot, Please type my \'/command\' for asks me. \nIf You\'re New Type \'/help\''\
            .format(user_name)
        chat = update["message"]["chat"]["id"]
        send_message(text, chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Welcome Sir, I'm Sinister Bot EiEi")

def menu(bot, update):
    keyboard = [[InlineKeyboardButton("Hello", callback_data='/hello'),
                 InlineKeyboardButton("What Time", callback_data='/what_time')],
                [InlineKeyboardButton("Option 3", callback_data='3'),
                 InlineKeyboardButton("Option 4", callback_data='4')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    update.dispatcher.add_handler(CallbackQueryHandler(button))
    update.idle()

def button(update, context):
    query = update.callback_query
    query.edit_message_text(text="Selected option: {}".format(query.data))

def hello(bot, update):
    bot.send_photo(chat_id=update.message.chat_id, photo='https://news.mthai.com/app/uploads/2019/02/a-7.jpg')

def what_time(bot, update):
    from datetime import datetime
    time_now = datetime.now().strftime('%H:%M:%S    %Y-%m-%d')
    bot.send_message(chat_id=update.message.chat_id, text=str(time_now))

def help(bot, update):
    help_text = """Please Type a Following '/command' to Let Me Help You ;) 
    Type '/start' : Start connect with me.
    Type '/hello' : Say hello to me
    Type '/menu' : Select a Function
    Type '/what_time' : Get the current time"""
    bot.send_message(chat_id=update.message.chat_id, text=help_text)

def main():
    last_update_id = None
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    while True:
        try:
            updates = get_updates(last_update_id)
            print(updates)
            get_message = str(updates['result'][0]['message']['text'])
            print(get_message)

            if get_message.startswith('/'):
                dispatcher.add_handler(CommandHandler('start', start))
                dispatcher.add_handler(CommandHandler('hello', hello))
                dispatcher.add_handler(CommandHandler('what_time', what_time))
                dispatcher.add_handler(CommandHandler('menu', menu))
                dispatcher.add_handler(CommandHandler('help', help))

                updater.start_polling()


            elif len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)

            time.sleep(0.2)

        except:
            pass


if __name__ == '__main__':
    main()

