#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import socketio
import json
import sys
from .constants import START_BOT, SEND_BOT_MESSAGE, BOT_MESSAGE_RECEIVED, BOT_MESSAGE_WATCHED, SEND_BOT_MESSAGE, SEND_BOT_MESSAGE, DELETE_BOT_MESSAGE, SET_BOT_KEYBOARD

sio = socketio.Client()
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def disconnect():
    print("I'm disconnected!")

def cb_start_bot(res):
  if 'error' in res:
    sio.disconnect()
  else:
    print('Бот успешно инициализирован')

def cb_send_message (res):
  if not res.get('id'):
    print('Не удалось отправить сообщение')

class Roschat_Bot():
  def __init__(self, token, base_url, bot_name, socket_options={'query': 'type-bot'}):
    self.token = token
    self.base_url = base_url
    self.bot_name = bot_name
    self.socket_options = socket_options

  def start(self):
    server_url = self.base_url + '/ajax/config.json'
    try:
      r = requests.get(server_url)
    except requests.exceptions.RequestException as e:
      print(e)
      sys.exit(1)
    server_config = json.loads(r.text)
    web_sockets_port = server_config.get('webSocketsPort')
    socket_url = self.base_url + ':' + web_sockets_port
    try:
      sio.connect(socket_url, headers=self.socket_options)
      sio.emit(
        START_BOT, 
        data={
          'token': self.token,
          'name': self.bot_name
        },
        callback=cb_start_bot
        )
    except ValueError:
      print(ValueError)

  def on(self, event_name, callback):
    sio.on(event_name, handler=callback)

  def emit(self, event_name, data, callback=None):
    sio.emit(event_name, data=data, callback=callback)

  def send_message(self, params, data, callback=cb_send_message):
    if not params:
      print('Для отправки сообщения необходим, как минимум cid пользователя')
    if type(params) is int:
      cid = params
      params = {
        'cid': cid,
        'data': data
      }
    elif type(params) is dict:
      if not params.get('cid'):
        print('Для отправки сообщения необходим cid пользователя')
        return
      params['data']=data
    sio.emit(SEND_BOT_MESSAGE, data=params, callback=callback)

  def send_message_received(self, msg_id, callback=None):
    if not msg_id:
      print('Обязательный параметр msg_id не предоставлен')
      return
    sio.emit(BOT_MESSAGE_RECEIVED, data={'id': msg_id}, callback=callback)

  def send_message_watched(self, msg_id, callback=None):
    if not msg_id:
      print('Обязательный параметр msg_id не предоставлен')
      return
    sio.emit(BOT_MESSAGE_WATCHED, data={'id': msg_id}, callback=callback)

  def delete_bot_message(self, msg_id, callback=None):
    if not msg_id:
      print('Обязательный параметр msg_id не предоставлен')
      return
    sio.emit(DELETE_BOT_MESSAGE, data={'id': msg_id}, callback=callback)

  def set_bot_keyboard(self, data):
    if not data.get('cid'):
      print('Обязательный поле cid не предоставлено')
      return
    sio.emit(SET_BOT_KEYBOARD, data=data)
