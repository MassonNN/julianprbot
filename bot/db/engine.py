"""
    Функции для работы с базой данных
"""
from typing import Union
from sqlalchemy import MetaData  # type: ignore
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine  # type: ignore
from sqlalchemy.engine import URL  # type: ignore
import sqlalchemy.ext.asyncio  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore


def create_async_engine(url: Union[URL, str]) -> sqlalchemy.ext.asyncio.AsyncEngine:
    """

    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=True, encoding='utf-8', pool_pre_ping=True)


@DeprecationWarning
async def proceed_schemas(engine: sqlalchemy.ext.asyncio.AsyncEngine, metadata: MetaData) -> None:
    """

    :param engine:
    :param metadata:
    """
    # async with engine.begin() as conn:
    #     await conn.run_sync(metadata.create_all)
    ...


def get_session_maker(engine: sqlalchemy.ext.asyncio.AsyncEngine) -> sessionmaker:
    """

    :param engine:
    :return:
    """
    return sessionmaker(engine, class_=sqlalchemy.ext.asyncio.AsyncSession, expire_on_commit=False)
