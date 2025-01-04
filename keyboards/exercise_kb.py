from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


async def get_exercise_kb(data: list[dict] = None) -> InlineKeyboardMarkup | None:
    if data is None:
        return
    buttons = []
    for button in data:
        buttons.append(
            [InlineKeyboardButton(text=button["name"], callback_data=f"ex%{button['name']}%{button['id']}")]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def get_yes_no_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="yes")],
        [InlineKeyboardButton(text="Нет", callback_data="no")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
