#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT, BOT_BUTTON_EVENT
import threading
from datetime import datetime, date, time

# Устанавливаем необходимые переменные 
user_cid = 3
time_interval = 30.0
message_text = "Сообщение по интервалу в " + str(time_interval) + " секунд"

# Инициализируем бота
bot = Roschat_Bot(
    token="f046fc088659498306a590276176c257fa99cf9fc46deacaa8d4736262d8d8f9",
    base_url="https://smolniy.ros.chat",
    bot_name="TETRA_BOT"
)
bot.start()

def cb_send_message(res):
    if not res.get('id'):
        print('Не удалось отправить сообщение')
    else:
        print('Сообщение доставлено пользователю')

# Отправка сообщения указанному пользователю по интервалу
def send_message_with_interval():
    threading.Timer(time_interval, send_message_with_interval).start()
    bot.send_message(
        user_cid,
        data=message_text,
        callback=cb_send_message
    )

send_message_with_interval()

# Обработка события 'bot-message-event' (сообщение от пользователя)
def on_message_event(*args):
    data = args[0]
    cid, data, id, dataType = [data[k] for k in ('cid', 'data', 'id', 'dataType')]

    
    if (dataType == 'unstored'): # Обрабатываем событие "пользователь пишет сообщение"
        print('Пользователь ', cid, ' пишет сообщение...')
        return
    bot.send_message_received(id)
    bot.send_message_watched(id)

    if (dataType == 'data'): # Обрабатываем НЕтекстовое сообщение
        bot.send_message(
            {
                'cid': cid,
                'dataType': 'data'
            },
            data
        )
    elif (dataType == 'text'): # Обрабатываем текстовое сообщение
        if data == '/start':
            bot.send_message(
                cid,
                data='Сейчас начнем',
                callback=cb_send_message
            )
        if data == '/date':
            bot.send_message(
                user_cid,
                data='Время сервера: ' + datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
                callback=cb_send_message
            )
        else:
            bot.send_message(
                cid,
                data='Неизвестная команда',
                callback=cb_send_message
            )

# Прослушка события 'bot-message-event' (сообщение от пользователя)
bot.on(BOT_MESSAGE_EVENT, on_message_event)
