# roschat-bot-python-sdk
Python SDK для написания ботов для сервера РОСЧАТ.

## Установка
Перед запуском необходимо заранее установить:
* python3.6
* pip
* virtualenv

Скопируйте репозиторий
```bash
git clone https://github.com/roschat/roschat-bot-python-sdk
cd roschat-bot-python-sdk
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
def on_bot_message
    # обработка события
bot.on(BOT_MESSAGE_EVENT, on_bot_message) # прослушивание входящего сообщения
```

Запустите скрипт командой:
```bash
python -m bot-dir # bot-dir — папка с вашим ботом
```