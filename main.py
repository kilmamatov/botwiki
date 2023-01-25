import telebot
import wikipedia
import re
import os



TOKEN = os.getenv('TELE_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    start_btn = telebot.types.KeyboardButton("/start")
    wiki_btn = telebot.types.KeyboardButton("/wiki")
    wikieng_btn = telebot.types.KeyboardButton("/wikieng")
    random_btn = telebot.types.KeyboardButton("/Random")
    markup.add(start_btn, wiki_btn, random_btn,wikieng_btn)
    bot.send_message(message.chat.id, 'Привет! Это бот wikipedia', reply_markup=markup)


wikipedia.set_lang('ru')


@bot.message_handler(commands=["Random"])
def random(m):
    bot.send_message(m.chat.id, 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["wiki"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение')

    def getwiki(s):
        try:
            ny = wikipedia.page(s)
            # Получаем первую тысячу символов
            wikitext = ny.content[:1000]
            # Разделяем по точкам
            wikimas = wikitext.split('.')
            # Отбрасываем всЕ после последней точки
            wikimas = wikimas[:-1]
            # Создаем пустую переменную для текста
            wikitext2 = ''
            # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
            for x in wikimas:
                if not ('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                    if (len((x.strip())) > 3):
                        wikitext2 = wikitext2 + x + '.'
                else:
                    break
            # Теперь при помощи регулярных выражений убираем разметку
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
            # Возвращаем текстовую строку
            return wikitext2
        # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
        except Exception as e:
            return 'В энциклопедии мало информации, подробнее по ссылке'

    # Получение сообщений от юзера
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Полная статья', url='https://ru.wikipedia.org/w/index.php?go=Перейти&search=' + message.text)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, getwiki(message.text), reply_markup=markup)


@bot.message_handler(commands=["wikieng"])
def start(m, res=False):
    wikipedia.set_lang('en')
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Английском языке')

    def getwiki(s):
        try:
            ny = wikipedia.page(s)
            # Получаем первую тысячу символов
            wikitext = ny.content[:1000]
            # Разделяем по точкам
            wikimas = wikitext.split('.')
            # Отбрасываем всЕ после последней точки
            wikimas = wikimas[:-1]
            # Создаем пустую переменную для текста
            wikitext2 = ''
            # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
            for x in wikimas:
                if not ('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                    if (len((x.strip())) > 3):
                        wikitext2 = wikitext2 + x + '.'
                else:
                    break
            # Теперь при помощи регулярных выражений убираем разметку
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
            # Возвращаем текстовую строку
            return wikitext2
        # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
        except Exception as e:
            return 'В энциклопедии мало информации, подробнее по ссылке'

    # Получение сообщений от юзера
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_my_site = telebot.types.InlineKeyboardButton(text='Full', url='https://en.wikipedia.org/w/index.php?search=&title=Special:Search' + message.text)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, getwiki(message.text), reply_markup=markup)


bot.polling(none_stop=True, interval=0)