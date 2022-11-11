#  Copyright (c) 2022.

from sqlalchemy import ForeignKey, Integer, Column, Table  # type: ignore

from .base import Base

PostChannel = Table(
    "post_channels",
    Base.metadata,  # type: ignore
    Column("post", ForeignKey("posts.id"), primary_key=True),
    Column("channel", ForeignKey("channels.id"), primary_key=True),
)
