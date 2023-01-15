#  Copyright (c) 2022.
from aiogram.types import Message


async def web_app_data_receive(message: Message):
    await message.answer(message.web_app_data.data)
