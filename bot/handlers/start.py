"""
    Файл хендлеров, связанных с командой /start
"""
from contextlib import suppress

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload  # type: ignore

from bot.db.user import get_user
from bot.structures.fsm_groups import PostStates
from bot.structures.keyboards import MENU_BOARD
from bot.structures.keyboards.posts_board import generate_posts_board


async def start(message: types.Message) -> None:
    """
    Хендлер для команды /start
    :param message:
    """
    await message.answer('Меню', reply_markup=MENU_BOARD)


async def call_start(call: types.CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер для команды /start
    :param call:
    :param state:
    """
    await state.clear()
    await call.message.answer('Меню', reply_markup=MENU_BOARD)
    with suppress(Exception):
        await call.message.delete()


async def menu_posts(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> None:
    """
    Хендлер для постов
    :param state:
    :param message:
    :param session_maker:
    """
    user = await get_user(user_id=message.from_user.id, session_maker=session_maker)
    await message.answer('Твои посты', reply_markup=generate_posts_board(posts=user.posts))
    await state.set_state(PostStates.waiting_for_select)


async def menu_channels(message: types.Message) -> None:
    """
    Хендлер для каналов
    :param message:
    """
    pass


async def menu_account(message: types.Message) -> None:
    """
    Хендлер для аккаунта
    :param message:
    """
    pass
