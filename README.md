# roschat-bot-python-sdk
Python SDK для написания ботов для сервера РОСЧАТ. [Описание протокола](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api) ботов.

## Установка
Перед запуском убедитесь, что у вас уже установлены:
* python3.6
* pip
* python3-venv

Скопируйте репозиторий
```bash
git clone https://github.com/roschat/roschat-bot-python-sdk
cd roschat-bot-python-sdk
python3 -m venv env
source env/bit/activate
pip install -r requirements.txt
```

## Начало работы
В папке для скриптов бота (далее в примере это папка `bot-dir`):

1. Создайте пустой файл `__init__.py`

2. Создайте файл `__main__.py`:
```py
# __main__.py
from .main import bot
```
3. Инициализируйте бота в файле `main.py`:
```py
from roschat.bot import Roschat_Bot
from roschat.constants import BOT_MESSAGE_EVENT

bot = Roschat_Bot(
    token="YOUR_BOT_TOKEN",
    base_url="YOUR_ROSCHAT_SERVER_ADDRESS",
    bot_name="YOUR_BOT_NAME"
  )
bot.start()
```

Запустите скрипт командой:
```bash
python -m bot-dir # bot-dir — папка с вашим ботом
```

## Пример работы с API
Обработка входящего события от сервера
```py
def on_bot_message(*args):
  data = args[0]
  bot.sendMessage(data['cid'], 'Тестовое сообщение') # отправка сообщения

bot.on(BOT_MESSAGE_EVENT, on_bot_message) # прослушивание входящего сообщения
```

## Методы Roschat_Bot
### Инициализация
__`start()`__

Создание сокет соединения с сервером и начало работы бота

### Работа с сообщениями
__`on(BOT_MESSAGE_EVENT, event_hadler)`__

Прослушивание события `bot-message-event` - входящее сообщении от пользователя

__`send_message({cid, dataType}, data[, callback])`__

или

__`send_message(cid, data[, callback])`__ - для отправки текстового сообщения

Отправить сообщения пользователю ([описание](
https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-send-bot-message
))

__`send_message_received(id[, callback])`__

Сообщить о получении сообщения пользователя ([описание](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-bot-message-received))

__`send_message_watched(id[, callback])`__

Сообщить о просмотре сообщения пользователя ([описание](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-bot-message-watched))

__`delete_bot_message(id[, callback])`__

Удалить сообщение в чате ([описание](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-delete-bot-message))

### Работа с клавиатурой
__`on(BOT_BUTTON_EVENT, function)`__

Событие `bot-button-event` - нажатие кнопки пользователем ([описание](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-bot-button-event))

__`set_bot_keyboard({cid, keyboard[, action]})`__

Установить клавиатуру в чате с пользователем ([описание](https://github.com/roschat/roschat-docs/wiki/roschat-bot-api-set-bot-keyboard))

## Пример бота
В папке [`example`](https://github.com/roschat/roschat-bot-python-sdk/tree/master/example) можно найти реализацию бота для сервера РОСЧАТ с использованием данного SDK. 
