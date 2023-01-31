from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def bot_echo(message: types.Message):
    text = [
        "Эхо без состояния.",
        "Сообщение:",
        message.text
    ]

    await message.answer('\n'.join(text))


async def bot_echo_all(message: types.Message, state: FSMContext, config):
    state_name = await state.get_state()

    if state_name == 'key_input':
        if message.text == config.tg_bot.user_key:
            await message.answer("Замечательно, вы ввели верный ключ! Перед демонстрацией меню, пожалуйста, напищите мне свои ФИО.")
            await state.set_state("full_name")
        else:
            await message.answer("Вы ввели неверный ключ, попробуйте ещё раз.")
    elif state_name == "full_name":
        await message.answer(f"Я получил ваши данные, {message.text}. Теперь выбирите, что хотите заказать.")
    else:
        text = (
            f'Эхо в состоянии {hcode(state_name)}\n',
            f'Содержание сообщения: {hcode(message.text)}',
        )
        await message.answer('\n'.join(text))


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
