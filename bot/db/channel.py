import datetime
from sqlalchemy import Column, Integer, VARCHAR, DATE, ForeignKey
from sqlalchemy.orm import relationship

from .post_channel import PostChannel
from .base import Base, Model


class Channel(Base, Model):
    __tablename__ = 'channels'

    # ID канала
    id = Column(Integer, unique=True, nullable=False, primary_key=True)

    admin_id = Column(Integer, ForeignKey('users.user_id'))
    admin = relationship('User', backref="channels")
    posts = relationship('Post', secondary=PostChannel, backref="channels")
    # Cтатистика
    subs_count = Column(Integer, nullable=False)


    def __str__(self) -> str:
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()

    @property
    def posts_count(self) -> int:
        return len(self.posts)

    @property
    def stats(self) -> str:
        return f"Подписчиков: {self.subs_count}"
