import asyncio

import pytest
import pytest_asyncio
from aiogram import Dispatcher, Bot
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from bot.db import create_async_engine
from bot.handlers import register_user_handlers
from mocked_bot import MockedBot


@pytest.fixture(scope="session")
def alembic_config():
    alembic_config = Config()
    alembic_config.set_main_option("file", "alembic.ini")
    alembic_config.set_main_option("script_location", "../bot/db/migrations")
    alembic_config.set_main_option("sqlalchemy.url", "postgresql+asyncpg://MassonNn@localhost/test")
    return alembic_config


@pytest.fixture(scope="session")
def revisions(alembic_config):
    revisions_dir = ScriptDirectory.from_config(alembic_config)
    revisions = list(revisions_dir.walk_revisions())
    revisions.reverse()
    return revisions


@pytest_asyncio.fixture(scope="session")
async def storage():
    tmp_storage = MemoryStorage()
    try:
        yield tmp_storage
    finally:
        await tmp_storage.close()


@pytest.fixture()
def bot():
    bot = MockedBot()
    token = Bot.set_current(bot)
    try:
        yield bot
    finally:
        Bot.reset_current(token)


@pytest_asyncio.fixture()
async def dispatcher():
    dp = Dispatcher()
    register_user_handlers(dp)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


@pytest_asyncio.fixture(scope="session")
async def engine(revisions, alembic_config):
    url = URL.create(
        "postgresql+asyncpg",
        username="MassonNn",
        host="localhost",
        database='test'
    )
    tmp_engine = create_async_engine(url=url)
    # setup_database(revisions, alembic_config)
    try:
        yield tmp_engine
    finally:
        await tmp_engine.dispose()
        # clear_database(revisions, alembic_config)


@pytest_asyncio.fixture(scope="session")
async def session_maker(engine: AsyncEngine):
    maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    try:
        yield maker
    finally:
        maker.close_all()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()
