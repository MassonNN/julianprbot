from aiogram import types
from aiogram.dispatcher.filters import CommandObject

from bot.commands.bot_commands import bot_commands


async def help_command(message: types.Message, command: CommandObject):
    if command.args:
        for cmd in bot_commands:
            if cmd[0] == command.args:
                return await message.answer(
                    f'{cmd[0]} - {cmd[1]}\n\n{cmd[2]}'
                )
        else:
            return await message.answer('Команда не найдена')
    return help_func(message)


async def help_func(message: types.Message):
    return await message.answer(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help <команда>\n'
    )


async def call_help_func(call: types.CallbackQuery):
    await call.message.edit_text(
        'Помощь и справка о боте\n'
        'Для того, чтобы получить информацию о команде используй /help <команда>\n',
        reply_markup=call.message.reply_markup
    )
