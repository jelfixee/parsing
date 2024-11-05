import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, F
from token import TOKEN
import pandas as pd

#index# item_category # price # title # date # store
#int# str # int # str # date

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Корзина продуктов")],
        [KeyboardButton(text="Цена продукта")]
    ], resize_keyboard=True)
    await message.answer("Выберете каталог", reply_markup=keyboard)

@dp.message(F.text == "Корзина продуктов")
async def product_search(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Магнит", callback_data="magnit")],
        [InlineKeyboardButton(text="Пятёрочка", callback_data="pyatyorochka")],
        #[InlineKeyboardButton(text="Семишагофф", callback_data="semishagof")],
        [InlineKeyboardButton(text="Ашан", callback_data="ashan")],
        [InlineKeyboardButton(text="Метро", callback_data="metro")],
        [InlineKeyboardButton(text="Окей", callback_data="okei")],
        [InlineKeyboardButton(text="Лента", callback_data="lenta")],
        #[InlineKeyboardButton(text="Перекрёсток", callback_data="perekryostok")]
    ])
    await message.answer("Выберете магазин", reply_markup=keyboard)

@dp.message(F.text == "Цена продукта")
async def product_search(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Хлеб", callback_data="hleb"), InlineKeyboardButton(text="Молоко", callback_data="moloko"), InlineKeyboardButton(text="Масло", callback_data="maslo")],
        [InlineKeyboardButton(text="Крупа", callback_data="krupa"), InlineKeyboardButton(text="Макароны", callback_data="makarony"), InlineKeyboardButton(text="Яйца", callback_data="aitsa")],
        [InlineKeyboardButton(text="Сосиски", callback_data="sosiski"), InlineKeyboardButton(text="Сыр", callback_data="syr"), InlineKeyboardButton(text="Мясо", callback_data="myaso")]
    ])
    await message.answer("Выберете раздел", reply_markup=keyboard)

@dp.callback_query()
def process_button(callback: CallbackQuery):

    categories = ["hleb", "moloko", "maslo", "krupa", "makarony", "aitsa", "sosiski", "syr", "myaso"]

    df = pd.read_csv("data.csv", index_col=0)

    if callback.data in categories:
        pass

    else:
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("Exit")