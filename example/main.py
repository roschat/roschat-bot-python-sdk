#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import json
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT, BOT_BUTTON_EVENT

bot = Roschat_Bot(
  token="15fa44b3492e8e77475412173c27b076da93409dbb02a7fa02d3aa8d857181c8",
  base_url="https://stand.ros.chat",
  bot_name="kill_net"
  )
bot.start()

def unpack_text_data(dataType, data) :
    if (dataType == 'text'):
      return data
    elif (dataType == 'data'):
      json_data = json.loads(data)
      text = None
      if 'text' in json_data :
          text = json_data['text']

      return text
    

def cb_send_message(res):
  if not res.get('id'):
    print('Не удалось отправить сообщение')
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
  cid, data, id, dataType, type = [data[k] for k in ('cid', 'data', 'id', 'dataType', 'type')]
  if (dataType == 'unstored'): return

  bot.send_message_received(id)
  bot.send_message_watched(id)

  text = unpack_text_data(dataType, data)
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

bot.on(BOT_MESSAGE_EVENT, on_message_event)
bot.on(BOT_BUTTON_EVENT, on_button_event)