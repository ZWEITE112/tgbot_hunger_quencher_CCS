from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def user_start(message: Message, state: FSMContext):
    await message.reply("Здраствуйте, чтобы активировать меня, введите секретный ключ.")
    await state.set_state('key_input')


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
