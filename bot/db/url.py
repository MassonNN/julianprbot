"""
    Ссылка в посте
"""
from sqlalchemy import Column, Integer, ForeignKey  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from .base import Base, Model  # type: ignore
from .types.url import URLType  # type: ignore


class URL(Base, Model):
    """Ссылка"""
    __tablename__ = 'urls'

    # ID поста
    url = Column(URLType, unique=True, nullable=False, primary_key=True)

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', backref="urls")

    # Cтатистика
    clicks_count = Column(Integer, default=0)

    def __init__(self, url: str):
        self.url = url

    @property
    def stats(self) -> str:
        """

        :return:
        """
        return f"Количество переходов: {self.clicks_count}"

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
