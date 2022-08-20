from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.db.user import is_user_exists, create_user


class RegisterCheck(BaseMiddleware):
    """
    Middleware будет вызываться каждый раз, когда пользователь будет отправлять боту сообщения (или нажимать
    на кнопку в инлайн-клавиатуре).
    """

    def __init__(self):
        """
        Не нужен в нашем случае
        """
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        """ Сама функция для обработки вызова """
        session_maker = data['session_maker']
        # Получаем менеджер сессий из ключевых аргументов, переданных в start_polling()
        if not await is_user_exists(user_id=event.from_user.id, session_maker=session_maker):
            await create_user(user_id=event.from_user.id,
                              username=event.from_user.username, session_maker=session_maker)
            await data['bot'].send_message(event.from_user.id, 'Ты успешно зарегистрирован(а)!')

        return await handler(event, data)
