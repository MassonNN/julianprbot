"""
    Пост
"""
import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, VARCHAR  # type: ignore
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import relationship  # type: ignore

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

    user_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', backref="posts")

    # Каналы, на которых он был опубликован
    # publicated_channel = relationship('Channel', secondary='PostChannel', back_populates="posts")

    def __init__(
            self,
            text: str,
            budget: int,
            pr_type: PRType,
            user_id: int,
            pub_price: float = 0.0,
            url_price: float = 0.0,
            subs_min: int = 0
    ):
        """
        :param text:
        :param budget:
        :param pr_type:
        :param user_id:
        :param pub_price:
        :param url_price:
        """
        self.text = text
        self.budget = budget
        self.pr_type = pr_type
        self.user_id = user_id
        self.pub_price = pub_price
        self.url_price = url_price
        self.subs_min = subs_min

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


class PostChannel(Base, CleanModel):
    """Таблица ассоциаций"""
    __tablename__ = 'post_channels'

    post = Column(Integer, ForeignKey('Post.id'), primary_key=True)
    channel = Column(Integer, ForeignKey('Channel.id'), primary_key=True)
