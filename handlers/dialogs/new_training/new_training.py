import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from api_requests import HistoryApi, TrainingApi


class NewTrainingStates(StatesGroup):
    save_name = State()
    save_description = State()

    current_bot_msg_id = None
    user_tg_id = None

class KeyboardManager:
    @staticmethod
    def get_cancel_keyboard():
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Отмена", callback_data="tr%cancel")]])

    @staticmethod
    def get_save_keyboard():
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Сохранить", callback_data="tr%save")],
            [InlineKeyboardButton(text="Отмена", callback_data="tr%cancel")]
        ])

class TrainingCreator:
    def __init__(self):
        pass

    async def create_training(self, name: str, description: str):
        client = TrainingApi()
        data = {
            "name": name,
            "description": description
        }
        return await client.send_post(data)

class DialogManager:
    def __init__(self, bot: Bot, dp: Dispatcher, keyboard_manager: KeyboardManager, training_creator: TrainingCreator):
        self.bot = bot
        self.dp = dp
        self.keyboard_manager = keyboard_manager
        self.training_creator = training_creator

    async def delete_previous_msg(self, state: FSMContext, obj: Message | CallbackQuery):
        message = obj.message if isinstance(obj, CallbackQuery) else obj
        if isinstance(obj, Message):
            await message.delete()
        current_data = await state.get_data()
        await self.bot.delete_message(chat_id=message.chat.id, message_id=current_data.get('current_bot_msg_id'))

    def setup_handlers(self):
        self.dp.message.register(self.input_new_training_name, Command(commands=["t"]))
        self.dp.message.register(self.input_new_training_description, NewTrainingStates.save_name)
        self.dp.message.register(self.confirm_new_training, NewTrainingStates.save_description)
        self.dp.callback_query.register(self.handle_callback, F.data.startswith("tr"))

    async def input_new_training_name(self, msg: Message, state: FSMContext):
        await state.set_state(NewTrainingStates.save_name)
        answer = await msg.answer("Введите название новой тренировки:", reply_markup=self.keyboard_manager.get_cancel_keyboard())
        await state.update_data(
            user_tg_id=msg.from_user.id,
            current_bot_msg_id=answer.message_id
        )

    async def input_new_training_description(self, msg: Message, state: FSMContext):
        await state.update_data(name=msg.text.capitalize())
        await state.set_state(NewTrainingStates.save_description)
        await self.delete_previous_msg(state, msg)
        answer = await msg.answer("Введите описание тренировки:", reply_markup=self.keyboard_manager.get_cancel_keyboard())
        await state.update_data(
            current_bot_msg_id=answer.message_id
        )

    async def confirm_new_training(self, msg: Message, state: FSMContext):
        await state.update_data(description=msg.text.capitalize())
        await self.delete_previous_msg(state, msg)
        data = await state.get_data()
        answer = await msg.answer(
            f"Название: {data['name']}\n"
            f"Описание: {data['description']}\n\n"
            "Сохранить тренировку?",
            reply_markup=self.keyboard_manager.get_save_keyboard()
        )
        await state.update_data(
            current_bot_msg_id=answer.message_id
        )

    async def handle_callback(self, cbq: CallbackQuery, state: FSMContext):
        await self.delete_previous_msg(state, cbq)
        action = cbq.data.split('%')[1]
        answer = None
        if action == "cancel":
            await state.clear()
            answer = await cbq.message.answer("Создание тренировки отменено.")
        elif action == "save":
            data = await state.get_data()
            result = await self.training_creator.create_training(data['name'], data['description'])
            if result:
                answer = await cbq.message.answer("Тренировка успешно создана!")
            else:
                answer = await cbq.message.answer("Произошла ошибка при создании тренировки.")
            await state.clear()
        if answer:
            await asyncio.sleep(5)
            await answer.delete()

def setup_new_training_dialog(dp: Dispatcher, bot: Bot):
    keyboard_manager = KeyboardManager()
    training_creator = TrainingCreator()
    dialog_manager = DialogManager(bot, dp, keyboard_manager, training_creator)
    dialog_manager.setup_handlers()