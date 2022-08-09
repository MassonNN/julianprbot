"""
    Структуры-шаблоны
"""
import re

from .cancel_board import cancel_board  # type: ignore

URL_CHECK = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
)  # type: ignore

__all__ = ['cancel_board', 'URL_CHECK']
