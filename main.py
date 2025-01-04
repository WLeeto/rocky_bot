import asyncio
import logging

from api_requests import ApiClient, HistoryApi
from create_bot import dp, bot
from handlers import admin, client
from handlers.dialogs.new_training import new_training
from handlers.dialogs.new_training.new_training import setup_new_training_dialog

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

# dialogs
setup_new_training_dialog(dp, bot)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())