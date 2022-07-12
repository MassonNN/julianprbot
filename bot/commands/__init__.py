__all__ = ['register_user_commands', 'bot_commands']

from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.command import CommandStart
from aiogram import F

from bot.commands.start import start
from bot.commands.help import help_command, help_func, call_help_func
from bot.commands.settings import settings_command, settings_callback
from bot.commands.callback_data_states import TestCallbackData
from bot.middlewares.register_check import RegisterCheck


def register_user_commands(router: Router) -> None:
    # router.message.register(start, Command(commands=['start']))
    router.message.register(start, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(start, F.text == 'Старт')
    router.message.register(help_func, F.text == 'Помощь')
    router.message.register(settings_command, Command(commands=['settings']))

    router.callback_query.register(call_help_func, F.data == 'help')
    router.callback_query.register(settings_callback, TestCallbackData.filter())

    router.message.register(RegisterCheck)
    router.callback_query.register(RegisterCheck)
