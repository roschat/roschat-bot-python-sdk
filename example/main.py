#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT, BOT_BUTTON_EVENT

bot = Roschat_Bot(
  token="8ed3e59c2c6df2deb4e98b81de5eadbc40cb151b8bb39aab7edd3084bfefb654",
  base_url="https://ormp.ros.chat",
  bot_name="NEW_BRAND_BOT"
  )
bot.start()

def cb_send_message(res):
  if not res.get('id'):
    print 'Не удалось отправить сообщение'
  else:
    print 'Сообщение доставлено пользователю'

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
  if (data.get('dataType') == 'unstored'):
    print '...'
    return
  cid, text, id = [data[k] for k in ('cid', 'data', 'id')]
  bot.send_message_received(id)
  bot.send_message_watched(id)
  if text == '/start':
    bot.send_message(
      cid,
      msg='Сейчас начнем',
      callback=cb_send_message
      )
  elif text == '/keyboard':
    bot.send_message(
      cid,
      msg='Отображаю клавиатуру',
      callback=cb_send_message
      )
    on_keyboard(cid)
  elif text == '/joke':
    bot.send_message(
      cid,
      msg='Загружаю шутку',
      callback=cb_send_message
      )
    on_keyboard(cid)
  else:
    bot.send_message(
      cid,
      msg='Неизвестная команда',
      callback=cb_send_message
      )

def on_button_event(*args):
  data = args[0]
  cid, callbackData = [data[k] for k in ('cid', 'callbackData')]
  if callbackData == 'joke':
    bot.send_message(
      cid,
      msg='Сейчас будут шутки'
    )
  elif callbackData == 'news':
    bot.send_message(
      cid,
      msg='Сейчас будут новости'
    )

bot.on(BOT_MESSAGE_EVENT, on_message_event)
bot.on(BOT_BUTTON_EVENT, on_button_event)