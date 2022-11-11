#  Copyright (c) 2022.

import asyncio
import logging
import os
import pathlib

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram.utils.i18n import I18n, ConstI18nMiddleware
from aioredis import Redis
from sqlalchemy.engine import URL  # type: ignore

from bot.db import create_async_engine, get_session_maker
from bot.handlers import register_user_commands
from bot.handlers.bot_commands import bot_commands
from bot.middlewares.register_check import RegisterCheck
from bot.utils import WORKDIR


async def bot_start(logger: logging.Logger) -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    redis = Redis(
        host=os.getenv('REDIS_HOST') or '127.0.0.1',
        password=os.getenv('REDIS_PASSWORD') or None,
        username=os.getenv('REDIS_USER') or None,
    )

    i18n = I18n(path=WORKDIR / 'locales', default_locale='ru', domain='messages')
    i18n_middleware = ConstI18nMiddleware(i18n=i18n, locale='ru')

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    i18n_middleware.setup(dp)

    bot = Bot(token=os.getenv('token'), parse_mode='HTML')  # type: ignore
    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("POSTGRES_USER"),
        host=os.getenv('POSTGRES_HOST'),
        database=os.getenv("POSTGRES_DB"),
        port=int(os.getenv("POSTGRES_PORT") or 0),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    # Делегировано alembic
    # await proceed_schemas(async_engine, BaseModel.metadata)
    await dp.start_polling(bot, session_maker=session_maker, logger=logger, redis=redis)


def setup_env():
    """Настройка переменных окружения"""
    from dotenv import load_dotenv
    path = pathlib.Path(__file__).parent.parent
    dotenv_path = path.joinpath('.env')
    if dotenv_path.exists():
        load_dotenv(dotenv_path)


def main():
    """Функция для запуска через poetry"""
    logger = logging.getLogger(__name__)
    try:
        setup_env()
        asyncio.run(bot_start(logger))
        logger.info('Bot started')
    except (KeyboardInterrupt, SystemExit):
        logger.info('Bot stopped')


if __name__ == '__main__':
    main()