''' Telegram bot Guess number v 0.2 / Телеграм бот Угадай число 0.2
autor s-evg https://github.com/s-evg'''
import telebot, random, os
from flask import Flask, request


TOKEN = os.environ.get('TOKEN')
APP_URL = f'https://guesssnumber.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


HELP = '''
Это бот "Угадай число".
Я загадываю число от 1 до 100,
а тебе нужно его угадать.
Если всё понятно жми: /newgame
/help запросить эту справку.
'''


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я бот "Угадай число.".\n' +
        'Давай поиграем?! Тогда быстрее жми /newgame.\n' +
        'Если нужна помошь, тогда тебе сюда: /help.'
  )


@bot.message_handler(commands=['help'])
def help(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Написать разработчику', url='telegram.me/s_evg13'
        )
    )
    bot.send_message(message.chat.id, HELP, reply_markup=keyboard)


@bot.message_handler(commands=['newgame'])
def newgame(message):
    # message.text
    global HiddenNumber
    global UserNumber
    HiddenNumber = random.randint(1, 100)
    print(message.text)
    print(HiddenNumber)
    text = message.text
    msg = bot.send_message(message.chat.id, 'Введи число от 1 до 100:')
    bot.register_next_step_handler(msg, GuessNumber)


def GuessNumber(message):
    text = message.text
    if not text.isdigit():              # проверка ввода пользователя на правильность
        msg = bot.send_message(message.chat.id, 'Вводить нужно число!')
        bot.register_next_step_handler(msg, GuessNumber)
        return

    if text != HiddenNumber:         # Собственно самая главная функция в этом боте!
        print(message.text)             # Сравнение числа с загаданным.
        UserNumber = int(message.text)
        if UserNumber > HiddenNumber:
            msg = bot.send_message(message.chat.id, 'Число должно быть меньше!')
            bot.register_next_step_handler(msg, GuessNumber)
        elif UserNumber < HiddenNumber:
            msg = bot.send_message(message.chat.id, 'Число должно быть больше!')
            bot.register_next_step_handler(msg, GuessNumber)
        else:
            bot.send_message(message.chat.id, 'Ты угадал, это число: ' + str(HiddenNumber))
            bot.send_message(message.chat.id, 'Начать новую игру: /newgame' )

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
