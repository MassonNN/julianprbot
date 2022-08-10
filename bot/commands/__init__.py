__all__ = ['register_user_commands', 'bot_commands']

from aiogram import F
from aiogram import Router
from aiogram.dispatcher.filters import Command, ContentTypesFilter
from aiogram.dispatcher.filters.command import CommandStart

from bot.commands.help import help_command, help_func, call_help_func
from bot.commands.start import (
    start,
    menu_posts,
    menu_account,
    menu_channels,
    menu_posts_create,
    menu_posts_get,
    menu_posts_create_url,
    menu_posts_create_text,
    menu_posts_create_prtype,
    menu_posts_create_prtype_pub,
    menu_posts_create_prtype_url,
    menu_posts_create_subs_min,
    PostStates
)
from bot.middlewares.register_check import RegisterCheck
from bot.structures.callback_data_factories import PostCallbackData


def register_user_commands(router: Router) -> None:
    """
    Зарегистрировать хендлеры пользователя
    :param router:
    """
    router.message.register(start, CommandStart())
    router.message.register(help_command, Command(commands=['help']))
    router.message.register(start, F.text == 'Старт')
    router.message.register(menu_posts, F.text == 'Твои посты')
    router.message.register(menu_account, F.text == 'Аккаунт')
    router.message.register(menu_channels, F.text == 'Твои каналы')
    router.message.register(menu_posts_create, F.data == 'createpost', PostStates.waiting_for_select)
    router.message.register(menu_posts_get, PostCallbackData.filter(), PostStates.waiting_for_select)
    router.message.register(menu_posts_create_text, PostStates.waiting_for_text)
    router.message.register(menu_posts_create_subs_min, PostStates.waiting_for_post_subs_min)
    router.message.register(menu_posts_create_prtype_url, PostStates.waiting_for_price_url)
    router.message.register(menu_posts_create_prtype_pub, PostStates.waiting_for_price_publication)
    router.message.register(menu_posts_create_prtype, PostStates.waiting_for_pr_type)
    router.message.register(menu_posts_create_url, PostStates.waiting_for_url, ContentTypesFilter(content_types=["sticker", "photo"]))
    router.message.register(help_func, F.text == 'Помощь')

    router.callback_query.register(call_help_func, F.data == 'help')

    router.message.register(RegisterCheck)
    router.callback_query.register(RegisterCheck)


# Alias
register_user_handlers = register_user_commands
