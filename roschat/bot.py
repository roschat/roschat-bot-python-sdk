#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import requests
import socketio
import json
import sys
from time import sleep
from .constants import START_BOT, SEND_BOT_MESSAGE, BOT_MESSAGE_RECEIVED, BOT_MESSAGE_WATCHED, SEND_BOT_MESSAGE, SEND_BOT_MESSAGE, DELETE_BOT_MESSAGE, SET_BOT_KEYBOARD

http_session = requests.Session()
http_session.verify = False
# sio = socketio.Client(http_session=http_session, logger=True, engineio_logger=True)
sio = socketio.Client(http_session=http_session)

@sio.event
def disconnect():
    print("Socket соединение разорвано")

def cb_start_bot(res):
  if 'error' in res:
    sio.disconnect()
    print('Ошибка при инициализации: ', res)
  else:
    print('Бот успешно инициализирован')

def cb_send_message(res):
  if not res.get('id'):
    print('Не удалось отправить сообщение', res)
class Roschat_Bot():
  def __init__(self, token, base_url, bot_name, socket_options={'query': 'type-bot', 'rejectUnauthorized': 'false'}):
    self.token = token
    self.base_url = base_url
    self.bot_name = bot_name
    self.socket_options = socket_options

  def start(self, on_start):
    server_url = self.base_url + '/ajax/config.json'
    self.on_start = on_start
    try:
      r = requests.get(server_url, verify=False)
    except requests.exceptions.RequestException as e:
      print(e)
      sys.exit(1)
    server_config = json.loads(r.text)
    web_sockets_port = server_config.get('webSocketsPortVer4')
    socket_url = str(self.base_url) + ':' + str(web_sockets_port)
    try:
      sio.on('connect', self.on_connected)
      sio.connect(socket_url, headers=self.socket_options)

    except ValueError:
      print(ValueError)
  
  def on_connected (self):
    print("Соединился с socket сервером...")

    sleep(2)

    print("Стартую бота...")
    self.start_bot()

  def start_bot(self):
    sio.emit(
      START_BOT, 
      data={
        'token': self.token,
        'name': self.bot_name
      },
      callback=self.on_start
    )

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
    params['data'] = data if isinstance(data, str) else json.dumps(data)
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
