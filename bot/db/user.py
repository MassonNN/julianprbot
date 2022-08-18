"""
    Модель пользователя
"""
from sqlalchemy import Column, Integer, VARCHAR, select, BigInteger  # type: ignore
from sqlalchemy.orm import sessionmaker, relationship, selectinload  # type: ignore

from .base import Base, Model  # type: ignore


class User(Base, Model):
    """
        Класс пользователя
    """
    __tablename__ = 'users'

    # Telegram user id
    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    # EUR
    balance = Column(Integer, default=0)
    posts = relationship('Post', back_populates="author", lazy=False)

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


async def get_user(user_id: int, session_maker: sessionmaker) -> User:
    """
    Получить пользователя по его id
    :param user_id:
    :param session_maker:
    :return:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(selectinload(User.posts))
                .filter(User.user_id == user_id)  # type: ignore
            )
            return result.scalars().one()
