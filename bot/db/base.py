"""
    Базовые классы базы данных
"""
#  Copyright (c) 2022.

from abc import abstractmethod
from datetime import date, timedelta, datetime as dt

from sqlalchemy import Column, DateTime  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore

Base = declarative_base()


class CleanModel:
    """
        Базовая модель в базе данных
    """
    creation_date = Column(DateTime, default=date.today())
    upd_date = Column(DateTime, onupdate=date.today())

    @property
    def no_upd_time(self) -> timedelta:
        """
        Получить время, которое модель не обновлялась
        :return: timedelta
        """
        return self.upd_date - dt.now()  # type: ignore


class Model(CleanModel):
    """
        Базовая бизнес-модель в базе данных
    """
    @property
    @abstractmethod
    def stats(self) -> str:
        """
        Функция для обработки и получения в строковом формате
        статистики модели (пользователя, ссылки, поста или канала)
        :return:
        """
        ...
