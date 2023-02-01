import asyncio
import logging

from bot_cls import MainCls, bot_cls
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.callback import register_callback
from tgbot.handlers.user import register_user
from tgbot.handlers.echo import register_echo
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.misc.bl import check_readiness

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    register_callback(dp)
    register_user(dp)

    register_echo(dp)


async def main(bot_cls: MainCls):
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    bot_cls.bot['config'] = bot_cls.config

    register_all_middlewares(bot_cls.dp, bot_cls.config)
    register_all_filters(bot_cls.dp)
    register_all_handlers(bot_cls.dp)

    bot_cls.initializer.run()

    check_readiness()


    # start
    try:
        await bot_cls.dp.start_polling()
    finally:
        await bot_cls.dp.storage.close()
        await bot_cls.dp.storage.wait_closed()
        await bot_cls.bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main(bot_cls))
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
