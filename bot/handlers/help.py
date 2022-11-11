"""
    Помощь
"""

#  Copyright (c) 2022.

from aiogram import types
from aiogram.filters import CommandObject
from aiogram.utils.i18n import gettext as _

from bot.handlers.bot_commands import bot_commands


async def help_command(message: types.Message, command: CommandObject):
    """
    Хендлер для помощи о команде
    :param message:
    :param command:
    :return:
    """
    if command.args:
        for cmd in bot_commands:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} - {cmd[1]}\n\n{cmd[2]}'
                )
        else:
            return await message.answer(_('Команда не найдена'))
    return help_func(message)


async def help_func(message: types.Message):
    """

    :param message:
    :return:
    """
    return await message.answer(
        _('Помощь и справка о боте\n'
          'Для того, чтобы получить информацию о команде используй /help <команда>\n')
    )


async def call_help_func(call: types.CallbackQuery):
    """
    Вызов помощи
    :param call:
    """
    await call.message.edit_text(  # type: ignore
        _('Помощь и справка о боте\n'
          'Для того, чтобы получить информацию о команде используй /help <команда>\n'),
        reply_markup=call.message.reply_markup  # type: ignore
    )
