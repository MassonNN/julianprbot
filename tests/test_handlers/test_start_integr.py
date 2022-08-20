import pytest
from aiogram import Dispatcher, Bot
from aiogram.methods import SendMessage

from bot.structures.keyboards import MENU_BOARD
from utils import get_update, get_message


@pytest.mark.asyncio
async def test_start_command(dispatcher: Dispatcher, bot: Bot):
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=get_message(text='/start')))
    assert isinstance(result, SendMessage)
    assert result.text == 'Меню'
    assert result.reply_markup == MENU_BOARD
