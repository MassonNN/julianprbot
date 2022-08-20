"""
    Пост
"""
import enum
import logging

from sqlalchemy import Column, Integer, ForeignKey, Enum, VARCHAR, select  # type: ignore
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, sessionmaker, Session  # type: ignore

from .base import Base, Model
from .post_channel import PostChannel
from .url import URL


class PRType(enum.Enum):
    """
        Типы раскрутки
    """
    NONE = 0            # не установлен
    CLICKS = 1          # переходы по ссылке
    PUBLICATIONS = 2    # публикации


class Post(Base, Model):
    """Модель поста"""
    __tablename__ = 'posts'

    # ID поста
    id = Column(Integer, autoincrement=True, primary_key=True)
    text = Column(TEXT, nullable=False)
    budget = Column(Integer, default=0)
    pr_type = Column(Enum(PRType), default=PRType.NONE)
    pub_price = Column(Integer, nullable=False, default=0)
    url_price = Column(Integer, nullable=False, default=0)
    subs_min = Column(Integer, nullable=False, default=0)
    author_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', back_populates="posts", lazy=False)

    # Каналы, на которых он был опубликован
    publicated_channel = relationship('Channel', secondary=PostChannel, back_populates="posts", lazy=False)

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"


async def create_post(
        session_maker: sessionmaker,
        text: str,
        pr_type: PRType,
        author_id: int,
        budget=0,
        subs_min=0,
        pub_price=None,
        url_price=None,
        url: str = ""
) -> Post | None:
    """
    Создать пост
    :param url:
    :param subs_min:
    :param session_maker:
    :param text:
    :param pr_type:
    :param author_id:
    :param budget:
    :param pub_price:
    :param url_price:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            post = Post(
                text=text,
                pr_type = pr_type,
                author_id = author_id,
                budget = budget,
                subs_min = subs_min,
            )
            post.urls = [URL(url=text), ]
            if pub_price:
                post.pub_price = pub_price
            elif url_price:
                post.url_price = url_price
            session: AsyncSession | Session
            try:
                session.add(post)
            except ProgrammingError as e:
                logging.error(e)
                return None
            else:
                return post


async def get_post(post_id: int, session_maker: sessionmaker) -> Post:
    async with session_maker() as session:
        async with session.begin():
            return (await session.execute(select(Post).where(Post.id == post_id))).scalars().unique().one_or_none()
