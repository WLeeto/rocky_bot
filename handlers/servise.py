from aiogram import types

from api_requests import UsersApi


async def get_user(event: types.Message | types.CallbackQuery) -> dict | None:

    if isinstance(event, types.CallbackQuery):
        user_id = event.from_user.id
        msg = event.message
    else:
        user_id = event.from_user.id
        msg = event


    api_client = UsersApi()
    user = await api_client.get_user_by_tg_id(user_id)

    if user:
        return user

    print(f"Cant find user by tg_id: {user_id}.")
    await msg.answer("Пользователь не найден в бд или нет подключения к бэку. "
                     "Все пропало, смотри логи. Заодно придумай нормальное сообщение об ошибке.")
    return