import os
import asyncio
import logging
from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from sqlalchemy.engine import URL

from bot.db import create_async_engine, get_session_maker, proceed_schemas
from bot.middlewares.register_check import RegisterCheck
from bot.commands import register_user_commands
from bot.commands.bot_commands import bot_commands
from bot.db.base import BaseModel


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()

    dp.message.middleware(RegisterCheck())
    dp.callback_query.middleware(RegisterCheck())

    bot = Bot(token=os.getenv('token'))
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
    await proceed_schemas(async_engine, BaseModel.metadata)
    await dp.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
