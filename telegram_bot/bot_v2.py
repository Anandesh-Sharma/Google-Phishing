import telebot
from config import telegram_token
from main import search_term
from helpers import fetch_dns
import pymongo
from config import mongo_username, mongo_password
import requests

bot = telebot.TeleBot(telegram_token)

client = pymongo.MongoClient('mongodb://{}:{}@localhost:27017'.format(mongo_username, mongo_password))
commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
}

hideBoard = telebot.types.ReplyKeyboardRemove()
cid = None
m = None
reporting_links_index = []
all_links = []
ev_links = []
keyword = None


@bot.message_handler(commands=['start'])
def return_links(message):
    global cid
    global m
    m = message
    cid = message.chat.id
    # reply keyboard
    reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add(telebot.types.KeyboardButton(text='/start'))
    bot.send_message(chat_id=cid, text='Welcome to google report bot!', reply_markup=reply_markup)
    bot.send_message(chat_id=cid,
                     text="\nThis bot is able to report the links as per your request! \n\n")

    # command_help(message)
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    search = telebot.types.InlineKeyboardButton(text='Search & Report', callback_data='search')
    ping = telebot.types.InlineKeyboardButton(text='Ping url', callback_data='ping')
    get_dns = telebot.types.InlineKeyboardButton(text='DNS info', callback_data='dns')
    cancel = telebot.types.InlineKeyboardButton(text='Previous Links', callback_data='pastlinks')

    markup.add(search, ping, get_dns, cancel)

    bot.send_message(chat_id=cid, text='Choose what you want to do ?', reply_markup=markup)


def get_link_button(index, reported):
    global all_links
    if reported:
        all_links[index].text += '| 🟢'
    else:
        all_links[index].text = all_links[index].text.split('|')[0]


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global all_links
    if call.data == 'search':
        bot.send_message(chat_id=cid, text="Enter a keyword that you want to fetch ad-links for:", )
        bot.register_next_step_handler(m, search_keyword)
    if len(call.data) == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        index = int(call.data)
        if index not in reporting_links_index:
            # add it with green emoji
            reporting_links_index.append(index)
            get_link_button(index=index, reported=True)
        else:
            reporting_links_index.remove(index)
            get_link_button(index=index, reported=False)

        for link in all_links:
            markup.add(link)
        bot.edit_message_reply_markup(chat_id=cid, message_id=call.message.message_id, reply_markup=markup)

    if call.data == 'report':
        bot.send_message(chat_id=cid, text='Reporting in progress, and reported soon')
        links_ids = []
        for i in reporting_links_index:
            links_ids.append(ev_links[i])
        # check if reporting already exists
        x_rep = client['master']['links'].find_one({'keyword': keyword})
        if 'reporting_links' not in x_rep and links_ids:
            client['master']['links'].update_one({'keyword': keyword},
                                                 {'$set': {'reporting_links': links_ids}})
        else:
            for ad in links_ids:
                if ad['link'] in [j['link'] for j in x_rep['reporting_links']]:
                    continue
                else:
                    client['master']['links'].update_one({'keyword': keyword},
                                                         {'$push': {'reporting_links': ad}})
    if call.data == 'ping':
        message = bot.send_message(chat_id=cid, text="Please enter the url (format : domain.com) to check its status:")
        bot.register_next_step_handler(message=message, callback=check_url_status)

    if call.data == 'dns':
        message = bot.send_message(chat_id=cid,
                                   text="Please enter the url (format : domain.com) to fetch its dns info:")
        bot.register_next_step_handler(message=message, callback=get_dns_info)

    if call.data == 'pastlinks':
        bot.send_message(chat_id=cid, text='Here are the past links that were reported!')
        db_links = client['master']['links'].find()
        print(db_links)
        db_r_links = []
        for i in db_links:
            if 'reporting_links' in i:
                x = i['reporting_links']
                print(x)
                db_r_links += [j['link'] for j in x]
        if db_r_links:
            bot.send_message(chat_id=cid, text="{}".format('\n'.join(db_r_links)))
        else:
            bot.send_message(chat_id=cid, text="No links were reported!")


def get_dns_info(message):
    url = message.text
    info = fetch_dns(url=url)
    if info['status']:
        if info['dns_info']:
            ns = []
            for i in info['dns_info']['nameservers']:
                ns.append(i['ldhName'])
            registration = ''
            expiration = ''

            for i in info['dns_info']['events']:
                if i['eventAction'] == "registration":
                    registration = i['eventDate']
                if i['eventAction'] == "expiration":
                    expiration = i['eventDate']

            bot.send_message(chat_id=cid,
                             text="DNS info found : \nNameServers: \n{} \nDates: \nregistration : {} \nexpiration: {}".format(
                                 '\n'.join(ns), registration, expiration))
        else:
            bot.send_message(chat_id=cid, text=f"No information is available for {url}")
    else:
        bot.send_message(chat_id=cid, text=f"dns check failed : {info}")


def check_url_status(message):
    url = "http://www." + message.text
    try:
        code = requests.get(url).status_code
    except Exception as e:
        bot.send_message(chat_id=cid, text=f"URL is not valid, please try again. \nError : {str(e)}")
        return

    if code == 200:
        bot.send_message(chat_id=cid, text=f"{url} is live, request code : {code}")
    else:
        bot.send_message(chat_id=cid, text=f"{url} is not live, request code : {code}")


def search_keyword(message):
    global all_links, ev_links, reporting_links_index, keyword
    reporting_links_index = []
    all_links = []
    ev_links = []
    keyword = message.text
    while True:
        result = search_term(message.text)
        if result['status']:
            x = result['links_ids']
            break
        else:
            print("Retrying to search")

    ev_links = x
    print(message.text)
    links = [i['link'] for i in x]
    # add links to the database
    db_links = client['master']['links'].find_one({'keyword': message.text})
    if db_links:
        # -> check if a particular link already exists ?
        dbl = [i['link'] for i in db_links['ads']]
        for i in x:
            if i['link'] in dbl:
                continue
            else:
                client['master']['links'].update_one({'keyword': message.text},
                                                     {'$push': {'ads': i}})
    else:
        client['master']['links'].insert_one({'keyword': message.text,
                                              'ads': x})

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    for index, link in enumerate(links):
        button = telebot.types.InlineKeyboardButton(text=link, callback_data=str(index))
        all_links.append(button)
        markup.add(button)
    markup.add(telebot.types.InlineKeyboardButton(text='Done, report now!', callback_data='report'))
    all_links.append(telebot.types.InlineKeyboardButton(text='Done, report now!', callback_data='report'))

    bot.send_message(chat_id=cid,
                     text="Here are the ad-links scraped from google. \nChoose which one you want to report"
                     , reply_markup=markup)


# HELP
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)


bot.polling()
