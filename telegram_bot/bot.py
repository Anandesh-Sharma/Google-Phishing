import telebot
from config import telegram_token
from main import search_term
import pymongo
from config import mongo_username, mongo_password

client = pymongo.MongoClient('mongodb://{}:{}@localhost:27017'.format(mongo_username, mongo_password))
bot = telebot.TeleBot(telegram_token)

keyword = None
links = list()
reporting_links = list()


@bot.message_handler(commands=['connect'])
def show_current(message):
    cid = message.chat.id


@bot.message_handler(commands=['start'])
def return_links(message):
    cid = message.chat.id
    msg = bot.send_message(chat_id=cid,
                           text="Welcome to google report bot! \n Reply to the message with the keyword you'd like to scrape for. \n\n",)
    bot.register_next_step_handler(msg, get_the_keyword)


def gen_markup_search():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    search = telebot.types.KeyboardButton('Search', )
    cancel = telebot.types.KeyboardButton('Cancel')

    markup.add(search, cancel)
    return markup


def get_the_keyword(message):
    global links, keyword
    cid = message.chat.id
    keyword = message.text
    print(keyword)
    # links_ids = search_term(keyword)

    # add to keywords - links
    # db_data = {
    #     '_id': keyword,
    #     'all_links': links_ids,
    #     'report_links': []
    # }
    # ex_data = client['master']['links'].find_one({'_id': keyword})
    # if ex_data:
    #     db_data['all_links'] = list(set(db_data['all_links'] + ex_data['all_links']))
    # else:
    #     client['master']['links'].insert_one(db_data)
    # bot.send_message(chat_id=cid, text="Please select which urls you want to report:", reply_markup=gen_markup(links))
    # bot.register_next_step_handler(message, get_phishing_urls, links)


def gen_markup(links):
    markup = telebot.types.InlineKeyboardMarkup()
    for link in links:
        markup.add(telebot.types.InlineKeyboardButton(link, callback_data=link))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global reporting_links
    if call.data in reporting_links:
        reporting_links.remove(call.data)
        bot.answer_callback_query(call.id, 'deleted : ' + call.data)
    else:
        reporting_links.append(call.data)
        bot.answer_callback_query(call.id, 'selected : ' + call.data)


@bot.message_handler(commands=['report'])
def return_links(message):
    global keyword, links, reporting_links
    cid = message.chat.id
    ex_data = client['master']['links'].find_one({'_id': keyword})
    client['master']['links'].update_one({'_id': keyword}, {
        "$set": {'report_links': list(set(ex_data['report_links'] + reporting_links))}})
    bot.send_message(chat_id=cid, text='Added to the reporting queue, Thanks elliot')

    # reset the global variables
    keyword = None
    links = []
    reporting_links = []


@bot.message_handler(commands=['test'])
def test(message):
    message = telebot.types.InputTextMessageContent("this is a dummy text")
    x = telebot.types.InlineQueryResultArticle(id='test', title='This a test', input_message_content=message,
                                               reply_markup=gen_markup(links=['1', '2']))
    print(x.to_json())
    # bot.send_message(chat_id=message.chat.id, text="hi", reply_markup=x)


bot.polling()
