import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

# from bot_app.tgbot.dialog.bot_menu.selected import on_enter
from infrastructure.database.functions.repo import create_session_pool
# from tgbot.dialog.bot_menu.selected import getter_router
from tgbot.config import load_config
from tgbot.dialog import setup_dialogs
from tgbot.handlers.admin import admin_router
from tgbot.handlers.commands import commands_router
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.middlewares.db_middleware import DatabaseMiddleware
from tgbot.services import broadcaster
from tgbot.services.default_commands import set_default_commands
from tgbot.services.telegraph.uploader import TelegraphService
import betterlogging as bl

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await set_default_commands(bot)
    await broadcaster.broadcast(bot, admin_ids, "Бот був запущений")


def register_global_middlewares(dp: Dispatcher, config, session):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    dp.message.outer_middleware(DatabaseMiddleware(session))
    dp.callback_query.outer_middleware(DatabaseMiddleware(session))


async def connect_debugger():
    import pydevd_pycharm
    logger.info("Debug mode is on. Waiting for debugger...")
    connected = False
    while not connected:
        try:
            pydevd_pycharm.settrace('host.docker.internal', port=4200, stdoutToServer=True, stderrToServer=True)
            connected = True
        except Exception as e:
            logger.error(f"Failed to connect to debugger: {e}")
            await asyncio.sleep(1)


async def main():
    logger.info("Starting bot")
    config = load_config(".env")

    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)
    if config.DEBUG:
        await connect_debugger()

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    storage = RedisStorage.from_url(
        config.redis.dsn(),
        key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
    )

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    session = create_session_pool(config.db, echo=True)
    telegraph_uploader = TelegraphService()

    for router in [
        commands_router,
        admin_router,
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config, session)
    dp['session'] = session
    dp['telegraph_uploader'] = telegraph_uploader
    setup_dialogs(dp)

    await on_startup(bot, config.tg_bot.admin_ids)
    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Бот був вимкнений!")
