from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import functools

from aiogram.types import CallbackQuery

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.misc.total_price_counter import total_price_counter
from tgbot.models.main_courses import MainCourse
from tgbot.models.bakery import Bakery


async def button_choose_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "button_main_courses":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_main_courses_menu)
        await state.set_state("main_courses_menu")
        await callback_query.answer()
    elif callback_query.data == "button_bakery":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_bakery_menu)
        await state.set_state("bakery_menu")
        await callback_query.answer()
    elif callback_query.data == "button_ordering":
        total_price = str(total_price_counter.total_counter(0))
        await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard.kb_order_menu) #f"Полная стоимость вашего заказа: {total_price}руб.",
        await state.set_state("order_menu")
        await callback_query.answer()


async def kb_main_courses_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
    elif callback_query.data.startswith("button_main_courses"):
        main_course = bot_cls.sql.session.query(MainCourse).filter(
            MainCourse.id == int(callback_query.data[len("button_main_courses"):])
        ).first()
        second_courses_price = print(total_price_counter.total_counter(main_course.price))
        # print(second_courses_price)
        await callback_query.message.answer(f'{main_course.dish_name} - {main_course.price}')
        await callback_query.answer()


async def kb_bakery_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
    elif callback_query.data.startswith("button_bakery"):
        bakery = bot_cls.sql.session.query(Bakery).filter(
        Bakery.id == int(callback_query.data[len("button_bakery"):])
        ).first()
        baking_price = total_price_counter.total_counter(bakery.price)
        # print(baking_price)
        await callback_query.message.answer(f'{bakery.dish_name} - {bakery.price}')
        await callback_query.answer()


async def kb_order_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
    elif callback_query.data == "button_finish_ordering":
        await state.set_state("submitting_an_order_for_execution")
        await callback_query.answer("Мы получили ваш заказ, ждите сообщения о его готовности. "
                                    "Спасибо, что выбрали нас!", show_alert=True)
        # types.ReplyKeyboardRemove()


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(button_choose_menu, state="view_menu")
    dp.register_callback_query_handler(kb_main_courses_menu, state="main_courses_menu")
    dp.register_callback_query_handler(kb_bakery_menu, state="bakery_menu")
    dp.register_callback_query_handler(kb_order_menu, state="order_menu")
