import pathlib
import os
from aiogram import Bot, Dispatcher, executor

from bot_mother_readdly.commands import set_bot_commands
from bot_mother_readdly.handlers import show_menu
from base.utils.storage import load_users


async def on_startup(dp: Dispatcher):
    await set_bot_commands(dp)
    dp.data['storage'] = os.path.join(pathlib.Path(__file__).parent, "storage")
    dp.data['users'] = load_users(dp.data['storage'])
    dp.register_message_handler(show_menu, commands=["start"])


async def on_shutdown(dp: Dispatcher):
    dp.stop_polling()
    await dp.wait_closed()


def main():
    bot = Bot("")
    dispatcher = Dispatcher(bot)
    executor.start_polling(
        dispatcher=dispatcher,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True
    )


if __name__ == "__main__":
    main()
