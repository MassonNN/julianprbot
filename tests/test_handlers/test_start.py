#  Copyright (c) 2022.

from unittest.mock import AsyncMock

import pytest
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey

from bot.handlers.start import start, call_start, menu_posts
from bot.structures.fsm_groups import PostStates
from bot.structures.keyboards import MENU_BOARD
from utils import TEST_USER, TEST_USER_CHAT


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await start(message)
    message.answer.assert_called_with('Меню', reply_markup=MENU_BOARD)


@pytest.mark.asyncio
async def test_start_callback_handler(storage, bot):
    call = AsyncMock()
    state = FSMContext(
        bot=bot,
        storage=storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_USER_CHAT.id)
    )

    await call_start(call=call, state=state)
    assert await state.get_state() is None

    call.message.delete.assert_any_call()
    call.message.answer.assert_called_with('Меню', reply_markup=MENU_BOARD)


@pytest.mark.asyncio
async def test_menu_posts(session_maker, bot, storage):
    message = AsyncMock()
    state = FSMContext(
        bot=bot, storage=storage,
        key=StorageKey(user_id=TEST_USER.id, bot_id=bot.id, chat_id=TEST_USER_CHAT.id)
    )
    await menu_posts(message=message, session_maker=session_maker, state=state)

    assert await state.get_state() == PostStates.waiting_for_select
    assert 'Твои посты' in message.answer.call_args
