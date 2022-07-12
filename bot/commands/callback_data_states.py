from aiogram.dispatcher.filters.callback_data import CallbackData


class TestCallbackData(CallbackData, prefix="test"):
    """
    Внимание! Фабрики колбеков будут удалены в следующих обновлениях aiogram
    """
    text: str
    user_id: int