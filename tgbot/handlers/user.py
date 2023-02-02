from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.models.user import User


async def user_start(message: Message, state: FSMContext):
    await message.reply("Здраствуйте, чтобы активировать меня, введите секретный ключ.")
    await state.set_state('key_input')


async def check_secret_key(message: Message, state: FSMContext, config):
    if message.text == config.tg_bot.user_key:
        await message.answer("Замечательно, вы ввели верный ключ!")
        await state.set_state("full_name")
        await checkin_user_name(message, state)
    else:
        await message.reply("Вы ввели неверный ключ, попробуйте ещё раз.")


async def checkin_user_name(message: Message, state: FSMContext):
    user_model = bot_cls.sql.session.query(User).filter(User.tg_id == message.from_user.id).first()
    if user_model is None:
        await message.answer("Перед демонстрацией меню, пожалуйста, напищите мне свои ФИО.")
        await state.set_state('new_user')
    else:
        await message.answer(
            f"Рады снова вас видеть, {user_model.full_name}. Прошу, делайте свой заказ.",
            reply_markup=inline_keyboard.kb_menu
        )
        await state.set_state("view_menu")


async def new_user(message: Message, state: FSMContext):
    new_user_model = User(tg_id=message.from_user.id, full_name=message.text)
    bot_cls.sql.session.add(new_user_model)
    bot_cls.sql.protected_commit()
    await message.reply(
        f"Я получил ваши данные, {message.text}. Теперь выбирите, что хотите заказать.",
        reply_markup=inline_keyboard.kb_menu
    )
    await state.set_state("view_menu")


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(check_secret_key, state="key_input", content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(checkin_user_name, state="full_name", content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(new_user, state="new_user", content_types=types.ContentTypes.TEXT)
