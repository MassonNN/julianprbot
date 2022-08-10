"""
    Файл хендлеров, связанных с командой /start
"""

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder
)
from sqlalchemy import select  # type: ignore
from sqlalchemy.engine import ScalarResult
from sqlalchemy.orm import sessionmaker, joinedload  # type: ignore

from bot.db import User
from bot.db.post import PRType, Post
from bot.db.url import URL
from bot.structures.keyboards import CANCEL_BOARD


async def start(message: types.Message) -> None:
    """
    Хендлер для команды /start
    :param message:
    """
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text='Твои посты')
    menu_builder.button(text='Твои каналы')
    menu_builder.button(text='Аккаунт')
    await message.answer('Меню', reply_markup=menu_builder.as_markup(resize_keyboard=True))


class PostStates(StatesGroup):
    """
        Состояния для постов
    """
    waiting_for_select = State()
    waiting_for_text = State()
    waiting_for_url = State()
    waiting_for_budget = State()
    waiting_for_pr_type = State()
    waiting_for_price_url = State()  # ожидаем цену одного перехода по ссылке
    waiting_for_price_publication = State()  # ожидаем цену одной публикации
    waiting_for_post_subs_min = State()


async def menu_posts(message: types.Message, session_maker: sessionmaker, state: FSMContext) -> None:
    """
    Хендлер для постов
    :param state:
    :param message:
    :param session_maker:
    """
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(User)
                .options(joinedload(User.posts))
                .filter(User.user_id == message.from_user.id)  # type: ignore
            )
            user = result.unique().scalars().one()
            print(user)
            print(user.posts)
            # await message.answer('Твои посты', reply_markup=generate_posts_board(posts=user.posts))
            # await state.set_state(PostStates.waiting_for_select)


async def menu_posts_create(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер для создания поста
    :param state:
    :param message:
    """
    await state.set_state(PostStates.waiting_for_text)
    await message.answer('Отправь текст нового поста', reply_markup=CANCEL_BOARD)


async def menu_posts_create_text(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер для получения текста нового поста
    :param message:
    :param state:
    """
    if message.text == 'Отмена':
        await state.clear()
        return await start(message)
    await state.update_data(post_text=message.text)
    await state.set_state(PostStates.waiting_for_url)
    await message.answer('Хорошо! Теперь отправь мне ссылку, которая будет под постом.', reply_markup=CANCEL_BOARD)


async def menu_posts_create_url(message: types.Message, state: FSMContext) -> None:
    """
    Хендлер для получения ссылки под постом
    :param message:
    :param state:
    :return:
    """
    if message.text == 'Отмена':
        await state.clear()
        return await start(message)
    if URL_CHECK.match(message.text):  # type: ignore
        await state.update_data(post_url=message.text)
        await state.set_state(PostStates.waiting_for_pr_type)
        rkm_builder = ReplyKeyboardBuilder()
        rkm_builder.button('Оплата за одну публикацию')
        rkm_builder.button('Оплата за переход по ссылке')
        rkm_builder.button('Отмена')
        await message.answer(
            'Теперь выбери вариант раскрутки поста',
            reply_markup=rkm_builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer('Отправь мне ссылку, которая будет под постом.', reply_markup=CANCEL_BOARD)


async def menu_posts_create_prtype(message: types.Message, state: FSMContext):
    """
    Хендлер для выбора типа раскрутки
    :param message:
    :param state:
    :return:
    """
    match message.text:
        case 'Отмена':
            await state.clear()
            return await start(message)
        case 'Оплата за одну публикацию':
            await state.update_data(pr_type=PRType.PUBLICATIONS)
            await state.set_state(PostStates.waiting_for_price_publication)
            return await message.answer('Отправь цену одной публикации (в EUR)')
        case 'Оплата за переход по ссылке':
            await state.update_data(pr_type=PRType.CLICKS)
            await state.set_state(PostStates.waiting_for_price_url)
            return await message.answer('Отправь цену одного перехода по ссылке')


async def menu_posts_create_prtype_url(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    """
    Хендлер для получения цены за один переход по ссылке
    :param session_maker:
    :param message:
    :param state:
    """
    price: float
    try:
        price = float(message.text)  # type: ignore
    except TypeError:
        return await message.answer('Отправь цену в EUR')
    data = await state.get_data()
    post = Post(  # type: ignore
        text=data['post_text'],
        pr_type=data['pr_type'],
        user_id=message.from_user.id,  # type: ignore
        budget=0,
        url_price=price
    )
    url = URL(url=data['post_url'])  # type: ignore
    post.urls = [url, ]

    async with session_maker() as session:
        async with session.begin():
            await session.merge(post)

    await state.clear()
    await message.answer('Пост был успешно создан, теперь его можно рекламировать!')
    return await start(message)


async def menu_posts_create_prtype_pub(message: types.Message, state: FSMContext):
    """
    Хендлер для получения цены за одну публикацию
    :param message:
    :param state:
    """
    price: float
    try:
        price = float(message.text)  # type: ignore
    except TypeError:
        return await message.answer('Отправь цену в EUR')
    await state.update_data(price=price)
    await state.set_state(PostStates.waiting_for_post_subs_min)
    await message.answer('Укажи минимальное количество подписчиков, которое требуется для публикации поста')


async def menu_posts_create_subs_min(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    """

    :param message:
    :param state:
    :param session_maker:
    """
    subs_min: int
    try:
        subs_min = int(message.text)  # type: ignore
    except TypeError:
        return await message.answer('Отправь число подписчиков')
    data = await state.get_data()
    post = Post(  # type: ignore
        text=data['post_text'],
        pr_type=data['pr_type'],
        user_id=message.from_user.id,  # type: ignore
        budget=0,
        pub_price=data['price'],
        subs_min=subs_min
    )
    url = URL(url=data['post_url'])  # type: ignore
    post.urls = [url, ]

    async with session_maker() as session:
        async with session.begin():
            await session.merge(post)

    await state.clear()
    await message.answer('Пост был успешно создан, теперь его можно рекламировать!')
    return await start(message)


async def menu_posts_get(message: types.Message) -> None:
    """
    Хендлер для просмотра поста
    :param message:
    """
    pass


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
