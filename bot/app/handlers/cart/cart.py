from bot.dataframes.users.users import *
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from bot.app.keyboards.inline.inline import cart_keyboard, remove_cart_keyboard

cart_router = Router()


@cart_router.message(F.text == "Корзина продуктов")
async def add_search(message: Message):
    keyboard = cart_keyboard
    await message.answer("Выберите продукт", reply_markup=keyboard)


@cart_router.callback_query(lambda c: c.data == 'view_cart')
async def view_cart(callback: CallbackQuery):

    chat_id = callback.message.chat.id
    users = read_users()
    user_id = callback.from_user.id

    try:
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    except:
        add_user(user_id)
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    if cart.empty:
        await callback.message.answer(text="Ваша корзина пуста.", chat_id=chat_id)

    else:
        keyboard = remove_cart_keyboard
        await callback.message.answer(text=f"Ваша корзина:\n{"\n".join(cart)}", chat_id=chat_id, reply_markup=keyboard)


@cart_router.callback_query(lambda c: c.data.startswith('add_to_cart_'))
async def add_cart(callback: CallbackQuery):

    chat_id = callback.message.chat.id
    users = read_users()
    user_id = callback.from_user.id
    product = callback.data.split('_')[-1]

    try:
        put_product(users, product)

    except:
        add_user(user_id)
        put_product(users, product)

    await callback.message.answer(text=f"Вы добавили: {product}", chat_id=chat_id)


@cart_router.callback_query(lambda c: c.data == 'back_to_cart')
async def back_to_cart(callback: CallbackQuery):

    chat_id = callback.message.chat.id
    keyboard = cart_keyboard
    users = read_users()
    user_id = callback.from_user.id

    try:
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    except:
        add_user(user_id)
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    if cart:
        await callback.message.answer(text="Ваша корзина:", chat_id=chat_id, reply_markup=keyboard)

    else:
        await callback.message.answer(text="Ваша корзина пуста.", chat_id=chat_id)


@cart_router.callback_query(lambda c: c.data.startswith('remove_'))
async def remove_product(callback: CallbackQuery):

    chat_id = callback.message.chat.id
    users = read_users()
    user_id = callback.from_user.id
    product = callback.data.split('_')[-1]

    try:
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    except:
        add_user(user_id)
        cart = users.set_index("user_id").loc[user_id].dropna().keys()

    if product in cart:
        await delete_product(user_id, product)

        await callback.message.answer(text=f"Вы удалили {product} из корзины.", chat_id=chat_id)

    else:
        await callback.message.answer(text="Продукт не найден в корзине.", chat_id=chat_id)
