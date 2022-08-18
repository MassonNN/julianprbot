"""
    Для работы с URL
"""
import re
from abc import ABC

import sqlalchemy.types as types


URL_EXP = re.compile(
    'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
)


class URLTypeError(Exception):
    """
    URL Exception
    """
    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text


class URLType(types.TypeDecorator):
    """
    URLType для базы данных
    """
    impl = types.TEXT
    prefix = "URL:"

    def process_bind_param(self, value, dialect):
        """

        :param value:
        :param dialect:
        :return:
        """
        return value

    def process_result_value(self, value, dialect):
        """

        :param value:
        :param dialect:
        :return:
        """
        return value

    def copy(self, **kw):
        """

        :param kw:
        :return:
        """
        return URLType()
