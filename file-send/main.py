#!/usr/local/bin/python
#!/usr/local/bin/python
import json
from time import sleep
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT, BOT_BUTTON_EVENT
import requests

bot = Roschat_Bot(
    token="478b9f28bc4fd76788cdc3ea12131921bb11cd93e2b99fcf811de0fefc599abd",
    base_url="https://stand.ros.chat",
    bot_name="test_bot_123"
)


def on_bot_start(res):
    to_contact = 1465

    print('Загружаю файл')
    url = 'https://stand.ros.chat/messages/data'
    files = {'file': open('./file-send/sova.jpg', 'rb')}

    r = requests.post(url, files=files)

    upload_name = r.text
    print('Файл загружен: ', upload_name)

    print('Отправляю файл пользователю')

    bot.send_message(
        params={
            'cid': to_contact,
            'dataType': 'data'
        },
        data={
            'type': 'image',
            'name': 'sova',
            'extension': 'jpg',
            'file': upload_name,
            'previewFile': upload_name
        },
        callback=cb_send_message
    )

    bot.send_message(
        to_contact,
        data='Как дела?'
    )


def cb_send_message(res):
    if not res.get('id'):
        print('Не удалось отправить сообщение', res)
    else:
        print('Сообщение доставлено пользователю')


bot.start(on_bot_start)
