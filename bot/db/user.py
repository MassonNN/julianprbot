"""
    Модель пользователя
"""
from sqlalchemy import Column, Integer, VARCHAR, select  # type: ignore
from sqlalchemy.orm import sessionmaker, relationship  # type: ignore

from .base import Base, Model  # type: ignore


class User(Base, Model):
    """
        Класс пользователя
    """
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    # User баланс (in EUR)
    balance = Column(Integer, default=0)

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
