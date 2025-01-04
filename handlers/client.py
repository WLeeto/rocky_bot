import random

from bot_messages import new_training_group_notify
from create_bot import dp, bot
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from handlers.servise import get_user
from keyboards.exercise_kb import get_exercise_kb
from api_requests import UsersApi, TrainingApi, HistoryApi, UserGroupApi


@dp.message(Command(commands=["ex",]))
async def new_history(msg: Message):
    user = await get_user(msg)
    if not user:
        return

    api_client = TrainingApi()
    training_data = await api_client.get_all_trainings()
    if not training_data:
        await msg.answer("Нет упражнений в бд или нет подключения к бэку.")
        return

    text = "Потренировался? Чем похвастаешься?"
    keyboard = await get_exercise_kb(training_data)
    if not keyboard:
        await msg.answer("Нет упражнений в бд или нет подключения к бэку.")
        return
    await msg.answer(text, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("ex%"))
async def new_history(cbq: CallbackQuery):
    await cbq.message.delete()

    user = await get_user(cbq)
    if not user:
        return
    training_name = cbq.data.split("%")[1]
    training_id = cbq.data.split("%")[2]

    api_client = HistoryApi()
    result = await api_client.add_new_history({"user": user.get("user"), "training": training_id})
    if not result:
        await cbq.message.answer("Я не смог добавить в историю новую тренировку.")
        return

    await cbq.message.answer(f"Я добавил новую тренировку \"{training_name}\", так держать!")


    api_client = UserGroupApi()
    result = await api_client.get_groups_by_user_id(user.get("id"))
    if not result:
        await cbq.message.answer("Похоже у вас нет прикрепленных групп, так что хвастаться некому =-(")
        return

    for user_group in result:
        text = random.choice(new_training_group_notify).format(username=cbq.from_user.username, training_name=training_name)
        try:
            await bot.send_message(chat_id=user_group.get('group')['group_id'], text=text)
        except Exception as ex:
            print(f"Fail to send message to group {user_group.get('group')['group_name']}. Error: {ex}")


def register_handlers_client(dp: Dispatcher):
    dp.message.register(new_history, Command(commands=["ex",]))
