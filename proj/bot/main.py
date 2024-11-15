import asyncio
import pandas as pd
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, F
from ttoken import TOKEN

# index# item_category # price # title # date # store
# int# str # int # str # date # str

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Каталог магазинов"), KeyboardButton(text="Каталог продуктов")],
        [KeyboardButton(text="Корзина продуктов")]
    ], resize_keyboard=True)
    await message.answer("Выберите каталог", reply_markup=keyboard)


@dp.message(F.text == "Каталог магазинов")
async def product_search(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Магнит", callback_data="magnit")],
        [InlineKeyboardButton(text="Пятёрочка", callback_data="pyatyorochka")],
        # [InlineKeyboardButton(text="Семишагофф", callback_data="semishagof")],
        [InlineKeyboardButton(text="Ашан", callback_data="ashan")],
        [InlineKeyboardButton(text="Метро", callback_data="metro")],
        [InlineKeyboardButton(text="Окей", callback_data="okei")],
        [InlineKeyboardButton(text="Лента", callback_data="lenta")],
        # [InlineKeyboardButton(text="Перекрёсток", callback_data="perekryostok")]
    ])
    await message.answer("Выберите магазин", reply_markup=keyboard)


@dp.message(F.text == "Каталог продуктов")
async def product_search(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хлеб", callback_data="hleb"),
         InlineKeyboardButton(text="Молоко", callback_data="moloko"),
         InlineKeyboardButton(text="Масло", callback_data="maslo")],
        [InlineKeyboardButton(text="Крупа", callback_data="krupa"),
         InlineKeyboardButton(text="Макароны", callback_data="makarony"),
         InlineKeyboardButton(text="Яйца", callback_data="aitsa")],
        [InlineKeyboardButton(text="Сосиски", callback_data="sosiski"),
         InlineKeyboardButton(text="Сыр", callback_data="syr"),
         InlineKeyboardButton(text="Мясо", callback_data="myaso")]
    ])
    await message.answer("Выберите раздел", reply_markup=keyboard)


@dp.callback_query()
async def process_button(callback: CallbackQuery):

    df = pd.read_csv("data.csv", index_col=0).reset_index()

    categories = df.item_category.unique()
    stores = {"magnit": "Магнит", "pyatyorochka": "Пятёрочка", "ashan": "Ашан", "metro": "Метро", "okei": "Окей", "lenta": "Лента"}

    if callback.data in categories:

        sought_series = df.set_index("item_category").sort_values(by=[ "price", "store"]).loc[callback.data]  # not right

        median = sought_series.price.median()
        median_four_items = sought_series.price.iloc[:4].median()

        for index in range(4):
            item = sought_series.iloc[index]

            item_store = item.store
            price = item.price
            item_title = item.title

            await callback.message.answer(f"{item_title}\n\n{price}₽ | {item_store}")

        await callback.message.answer(f"Медиана по всем ценам: {round(median, 2)}₽\nМедиана по 4-м ценам: {round(median_four_items, 2)}₽")


    elif callback.data in stores.keys():

        items_sum = 0

        for category in categories:

            filtered_df = df.loc[(df['store'] == callback.data) & (df['item_category'] == category)]

            if not filtered_df.empty:

                title = filtered_df.iloc[0].title
                price = filtered_df.iloc[0].price
                items_sum += price

                await callback.message.answer(f"{title} {price}₽")

            else:
                await callback.message.answer(f"Все товары не найдены. ({stores[callback.data]}) ")

        await callback.message.answer(f"Всего {items_sum}₽")

    #elif callback.data:



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Exit")
