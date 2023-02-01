from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.models.main_courses import MainCourse


async def button_choose_menu(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'button_main_courses':
            await callback_query.message.edit_reply_markup(inline_keyboard.kb_main_courses_menu)
            await state.set_state('main_courses_menu')
        case 'button_bakery':
            await callback_query.message.edit_reply_markup(inline_keyboard.kb_bakery_menu)
            await state.set_state('kb_bakery_menu')


async def kb_main_courses_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'come_back':
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
    elif callback_query.data.startswith('button_main_courses'):
        main_course = bot_cls.sql.session.query(MainCourse).filter(
            MainCourse.id == int(callback_query.data[len('button_main_courses'):])
        ).first()

        await callback_query.message.answer(f'{main_course.dish_name} - {main_course.price}')


async def kb_bakery_menu(callback_query: types.CallbackQuery, state: FSMContext):
    match callback_query.data:
        case 'come_back':
            await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
            await state.set_state("view_menu")


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(button_choose_menu, state="view_menu")
    dp.register_callback_query_handler(kb_main_courses_menu, state="main_courses_menu")
    dp.register_callback_query_handler(kb_bakery_menu, state="kb_bakery_menu")
