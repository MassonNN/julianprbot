"""
    Ссылка в посте
"""

from sqlalchemy import Column, Integer, ForeignKey  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, sessionmaker  # type: ignore

from .base import Base, Model  # type: ignore
from .types.url import URLType  # type: ignore


class URL(Base, Model):
    """Ссылка"""
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(URLType, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', backref="urls", lazy=False)
    # Cтатистика
    clicks_count = Column(Integer, default=0)

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


async def create_url(session_maker: sessionmaker, url_text: str, post: Base):
    """
    Создать URL
    :param session_maker:
    :param url_text:
    :param post:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            post.urls.append(URL(
                url = url_text,
                post_id = post.id
            ))
