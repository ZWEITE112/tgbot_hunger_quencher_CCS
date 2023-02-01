from aiogram import Bot, Dispatcher

from tgbot.config import load_config
from tgbot.services.sql import SQL, Initializer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2


class MainCls:
    def __init__(self):
        self.config = load_config(".env")

        self.storage = RedisStorage2() if self.config.tg_bot.use_redis else MemoryStorage()
        self.bot = Bot(token=self.config.tg_bot.token, parse_mode='HTML')
        self.dp = Dispatcher(self.bot, storage=self.storage)
        self.sql = SQL(self.config)
        self.initializer = Initializer(self.config, self.sql)


bot_cls = MainCls()
