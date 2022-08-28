"""
    Файл запуска
"""
#  Copyright (c) 2022.

import asyncio
import logging
import os
import pathlib

from aiogram import Dispatcher, Bot, Router
from aiogram.dispatcher.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from sqlalchemy.engine import URL  # type: ignore

from bot.db import create_async_engine, get_session_maker
from bot.handlers import register_user_commands
from bot.handlers.bot_commands import bot_commands
from bot.middlewares.register_check import RegisterCheck
from bot.misc import redis


async def bot_start(logger: logging.Logger) -> None:
    """Запуск бота"""
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher(storage=RedisStorage(redis=redis))
    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    router = Router()
    dp.update.bind_filter()

    bot = Bot(token=os.getenv('token'), parse_mode='HTML')  # type: ignore
    await bot.set_my_commands(commands=commands_for_bot)
    register_user_commands(dp)

    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=os.getenv("db_user"),
        host="localhost",
        database=os.getenv("db_name"),
        port=os.getenv("db_port")
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
