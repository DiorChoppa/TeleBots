import telebot
import requests
from bs4 import BeautifulSoup as bs
import random
import time
URL_ENG = 'https://puzzle-english.com/directory/1000-popular-words'
URL_CURRENCY = 'https://finance.rambler.ru/currencies/'
TOKEN = '***'

bot = telebot.TeleBot(TOKEN)


def parse_currency():
    request = requests.get(URL_CURRENCY)
    soup = bs(request.text, 'html.parser')
    currency = soup.find_all('div', class_='currency-block__marketplace-value')
    wr = open('currency.txt', 'w', encoding='utf-8')
    for x in currency:
        wr.write(str(x).replace('<div class="currency-block__marketplace-value">', '').replace('</div>', ''))
    wr.close()
    rd = open('currency.txt', 'r', encoding='utf-8')
    a = ['USD вчера: ', '', 'USD сегодня: ', '', 'EURO вчера: ', '', 'EURO сегодня: ', '']
    h = 0
    for x in rd:
        if h == 1:
            a[1] = x
        elif h == 3:
            a[3] = x
        elif h == 9:
            a[5] = x
        elif h == 11:
            a[7] = x
        h += 1
    return ''.join(a)


def parse_words():
    request = requests.get(URL_ENG)
    soup = bs(request.text, 'html.parser')
    words = soup.find_all('li', style="font-weight: 400;")
    wr = open('words.txt', 'w', encoding='utf-8')
    ct = 0
    for word in words:
        ct += 1
        wr.write(str(word) + '\n')
        if ct >= 200:
            break
    wr.close()

    a = []
    rd = open('words.txt', 'r', encoding='utf-8')
    for word in rd:
        a.append(str(rd.readline())
                 .replace('<li style="font-weight: 400;"><span style="font-weight: 400;">', '')
                 .replace('</span><span style="font-weight: 400;">', '')
                 .replace('</span><span style="font-weight: 400;">', '')
                 .replace('</span></li>', ''))
    rd.close()

    wr = open('words.txt', 'w', encoding='utf-8')
    for x in a:
        wr.write(x)
    wr.close()


@bot.message_handler(content_types=['text'])
def send_words(message):
    if message.text == 'Слова':
        bot.send_message(message.from_user.id, 'Новые слова на сегодня:')   # user.chat.id
        for x in range(0, 5):
            bot.send_message(message.from_user.id, random.choice(open('words.txt', 'r', encoding='utf-8').readlines()))
    elif message.text == 'Курс':
        bot.send_message(message.from_user.id, 'Курс валют:')
        bot.send_message(message.from_user.id, f'{str(parse_currency())}')
    else:
        bot.send_message(message.from_user.id, message.text)


# Echo bot
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.rely_to(message, message.text)


if __name__ == '__main__':
    print('Launching...')
    parse_currency()
    parse_words()
    print('Parsed.')
    bot.polling(none_stop=True, interval=0)

'''
Сообщения от бота по расписанию:

@bot.message_handler(content_types=['text'])
def send_words(message, id):
    if message.text == 'Слова':
        bot.send_message(message.from_user.id, 'Новые слова на сегодня:')   # user.chat.id
        for x in range(0, 5):
            bot.send_message(message.from_user.id, random.choice(open('words.txt', 'r', encoding='utf-8').readlines()))
while True:
    send_words(message, id)
    time.sleep(60*60*24)
'''