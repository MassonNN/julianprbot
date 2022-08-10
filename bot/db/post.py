"""
    Пост
"""
import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, VARCHAR  # type: ignore
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import relationship  # type: ignore

from .post_channel import PostChannel
from bot.db.base import Base, Model, CleanModel
from bot.db.types.url import URLType


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
    id = Column(Integer, unique=True, nullable=False, primary_key=True)
    text = Column(TEXT, nullable=False)
    budget = Column(Integer, default=0)
    pr_type = Column(Enum(PRType), default=PRType.NONE)
    pub_price = Column(Integer, nullable=False, default=0)
    url_price = Column(Integer, nullable=False, default=0)
    subs_min = Column(Integer, nullable=False, default=0)

    author_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', backref="posts", innerjoin=True, lazy=False)

    # Каналы, на которых он был опубликован
    publicated_channel = relationship('Channel', secondary=PostChannel, backref="posts")

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"
