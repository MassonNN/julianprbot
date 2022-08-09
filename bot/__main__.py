"""
    Файл запуска
"""
import os
import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.engine import URL  # type: ignore

from bot.db import create_async_engine, get_session_maker
from bot.middlewares.register_check import RegisterCheck
from bot.commands import register_user_commands
from bot.commands.bot_commands import bot_commands


async def main() -> None:
    """
    функция входа
    """
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    bot = Bot(token=os.getenv('token'))  # type: ignore
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
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
