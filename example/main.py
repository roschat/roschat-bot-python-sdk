#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import json
from time import sleep
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT, BOT_BUTTON_EVENT

bot = Roschat_Bot(
    token="07cff473c113e8c46114849f9b1a2d2eb6e059f5665a67899155abdb2e68d5ea",
    base_url="https://10.10.38.191",
    bot_name="test_bot_123"
)


def unpack_text_data(dataType, data):
    if (dataType == 'text'):
        return data
    elif (dataType == 'data'):
        json_data = json.loads(data)
        text = None
        if 'text' in json_data:
            text = json_data['text']

        return text


def cb_send_message(res):
    if not res.get('id'):
        print('Не удалось отправить сообщение', res)
    else:
        print('Сообщение доставлено пользователю')


def on_keyboard(cid):
    keyboard = [
        [
            {
                'text': 'Шутка',
                'callbackData': 'joke'
            },
            {
                'text': 'Новости',
                'callbackData': 'news'
            }
        ]
    ]
    bot.set_bot_keyboard(
        data={
            'cid': cid,
            'keyboard': keyboard,
            'action': 'show'
        }
    )


def on_message_event(*args):
    data = args[0]

    cid = data.get('cid')
    msgData = data.get('data')
    id = data.get('id')
    dataType = data.get('dataType')
    cidType = data.get('cidType', 'user')

    if (dataType == 'unstored'):
        return

    print(f'cid: {cid}')
    print(f'id: {id}')
    print(f'cidType: {cidType}')
    print(f'dataType: {dataType}')
    print(f'msgData: {msgData}')

    bot.send_message_received(id)
    bot.send_message_watched(id)

    text = unpack_text_data(dataType, msgData)
    print(f'user text: {text}')
    if (not text):
        bot.send_message(
            cid,
            data='Я работаю только с текстовыми командами.',
            callback=cb_send_message
        )
    else:
        if text == '/start':
            bot.send_message(
                cid,
                data='Сейчас начнем',
                callback=cb_send_message
            )
        elif text == '/keyboard':
            bot.send_message(
                cid,
                data='Отображаю клавиатуру',
                callback=cb_send_message
            )
            on_keyboard(cid)
        elif text == '/joke':
            bot.send_message(
                cid,
                data='Загружаю шутку',
                callback=cb_send_message
            )
            on_keyboard(cid)
        else:
            bot.send_message(
                cid,
                data='Неизвестная команда',
                callback=cb_send_message
            )


def on_button_event(*args):
    data = args[0]
    cid, callbackData = [data[k] for k in ('cid', 'callbackData')]
    if callbackData == 'joke':
        bot.send_message(
            cid,
            data='Сейчас будут шутки'
        )
    elif callbackData == 'news':
        bot.send_message(
            cid,
            data='Сейчас будут новости'
        )


def on_bot_start(res):
    print('Бот успешно инициализирован и готов принимать и отправлять сообщения')


bot.start(on_bot_start)
bot.on(BOT_MESSAGE_EVENT, on_message_event)
bot.on(BOT_BUTTON_EVENT, on_button_event)

while True:
    sleep(1)