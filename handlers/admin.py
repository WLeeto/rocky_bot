from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup

from create_bot import dp

from aiogram.types import Message, CallbackQuery

from keyboards.exercise_kb import get_exercise_kb, test_exercise_data


@dp.message(Command(commands=['test', 'x']))
async def test(msg: Message):

    print(f"User: {msg.from_user.id} {msg.from_user.username}")
    print(f"Group: {msg.chat.id} {msg.chat.title}")

    await msg.answer(f"Rocky работает")


# @dp.message(Command(commands=['kb']))
# async def test_kb(msg: Message):
#     keyboard = await get_exercise_kb(test_exercise_data)
#     await msg.answer("Появится клавиатура", reply_markup=keyboard)


# @dp.callback_query()
# async def test_callback(cbq: CallbackQuery):
#     await cbq.message.delete_reply_markup()
#     await cbq.message.answer(f"Выбрано упражнение: {cbq.data}")



def register_handlers_admin(dp: Dispatcher):
    dp.message.register(test, Command(commands=['test', 'x']))