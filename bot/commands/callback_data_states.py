from aiogram.dispatcher.filters.callback_data import CallbackData


class TestCallbackData(CallbackData, prefix="test"):
    text: str
    user_id: int