from sqlalchemy import ForeignKey, Integer, Column, Table  # type: ignore

from .base import CleanModel, Base


PostChannel = Table(
    "post_channels",
    Base.metadata,
    Column("post", ForeignKey("posts.id")),
    Column("channel", ForeignKey("channels.id")),
)