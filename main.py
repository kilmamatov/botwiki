import telebot
import wikipedia
import re
import os
from telebot import types


TOKEN = os.getenv('TELE_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    start_btn = telebot.types.KeyboardButton("/start")
    wiki_btn = telebot.types.KeyboardButton("/wiki")
    markup.add(start_btn, wiki_btn)
    bot.send_message(message.chat.id, 'Привет! Это бот wikipedia', reply_markup=markup)


wikipedia.set_lang('ru')


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
            return 'В энциклопедии нет информации об этом'

    # Получение сообщений от юзера
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        markup = types.InlineKeyboardMarkup()
        btn_my_site = types.InlineKeyboardButton(text='Полная статья', url='https://ru.wikipedia.org/w/index.php?go=Перейти&search=' + message.text)
        markup.add(btn_my_site)
        bot.send_message(message.chat.id, getwiki(message.text), reply_markup=markup)


bot.polling(none_stop=True, interval=0)