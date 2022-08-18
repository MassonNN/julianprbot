from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from bot.db import User


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

        # Получаем менеджер сессий из ключевых аргументов, переданных в start_polling()
        session_maker: sessionmaker = data['session_maker']

        # добавляем асинхронный контекст
        async with session_maker() as session:

            # в синхронном режиме запускаем работу с сессией
            async with session.begin():

                # получаем результат выбора ВСЕХ пользователей ГДЕ user_id равен user_id из события (сообщения)
                result = await session.execute(select(User).where(User.user_id == event.from_user.id))

                # получаем и обрабатываем пользователя
                user: User = result.scalars().unique().one_or_none()

                if user is not None:
                    # значит пользователь уже зарегистрирован
                    pass
                else:
                    # следует зарегистрировать пользователя

                    # создаем экземпляр для нашего пользователя
                    user = User(
                        user_id=event.from_user.id,
                        username=event.from_user.username
                    )

                    # добавляем его в сессию
                    session.add(user)

                    if isinstance(event, Message):
                        await event.answer('Ты успешно зарегистрирован(а)!')
                    else:
                        await event.message.answer('Ты успешно зарегистрирован(а)!')

                    # контекстный менеджер session.begin() сам сохранит все изменения!!!

        # передаем управление в хендлер
        return await handler(event, data)
