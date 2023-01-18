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
    # lang1_btn = telebot.types.KeyboardButton("ru")
    # lang2_btn = telebot.types.KeyboardButton("en")
    markup.add(start_btn, wiki_btn)
    bot.send_message(message.chat.id, 'Привет! Это бот много чего умеет!(Выбери язык)', reply_markup=markup)


wikipedia.set_lang('ru')


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["wiki"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')

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
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
            wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
            # Возвращаем текстовую строку
            return wikitext2
        # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
        except Exception as e:
            return 'В энциклопедии нет информации об этом'

    # Получение сообщений от юзера
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        bot.send_message(message.chat.id, getwiki(message.text))


bot.polling(none_stop=True, interval=0)
