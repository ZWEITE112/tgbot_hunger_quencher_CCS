from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.models.main_courses import MainCourse
from tgbot.models.bakery import Bakery
from tgbot.models.order import Order
from tgbot.models.users import Users


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
        user_model = bot_cls.sql.session.query(Users).filter(Users.tg_id == callback_query.from_user.id).first()
        order = Order.get_or_create(user_model.id)

        await bot_cls.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text=f"Полная стоимость вашего заказа: {order.total_price}руб."
        )
        await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard.kb_order_menu)
        await state.set_state("order_menu")
        await callback_query.answer()


async def kb_main_courses_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
        await callback_query.answer()
    elif callback_query.data.startswith("button_main_courses"):
        user_model = bot_cls.sql.session.query(Users).filter(Users.tg_id==callback_query.from_user.id).first()

        main_course = bot_cls.sql.session.query(MainCourse).filter(
            MainCourse.id == int(callback_query.data[len("button_main_courses"):])
        ).first()

        order = Order.get_or_create(user_model.id)
        adding_name = main_course.dish_name if order.order_list=='' else f'|{main_course.dish_name}'
        order.order_list += adding_name
        order.total_price += main_course.price
        bot_cls.sql.protected_commit()

        await callback_query.message.answer(f'{main_course.dish_name} - {main_course.price}')
        await callback_query.answer()


async def kb_bakery_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
        await callback_query.answer()
    elif callback_query.data.startswith("button_bakery"):
        user_model = bot_cls.sql.session.query(Users).filter(Users.tg_id == callback_query.from_user.id).first()

        bakery = bot_cls.sql.session.query(Bakery).filter(
            Bakery.id == int(
                callback_query.data[len("button_bakery"):]
            )
        ).first()

        order = Order.get_or_create(user_model.id)
        adding_name = bakery.dish_name if order.order_list == '' else f'|{bakery.dish_name}'
        order.order_list += adding_name
        order.total_price += bakery.price
        bot_cls.sql.protected_commit()
        await callback_query.message.answer(f'{bakery.dish_name} - {bakery.price}')
        await callback_query.answer()


async def kb_order_menu(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "come_back":
        await bot_cls.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            text="Я вас не тороплю, можете продолжать выбирать блюда."
        )
        await callback_query.message.edit_reply_markup(inline_keyboard.kb_menu)
        await state.set_state("view_menu")
        await callback_query.answer()
    elif callback_query.data == "button_finish_ordering":
        user_model = bot_cls.sql.session.query(Users).filter(Users.tg_id==callback_query.from_user.id).first()

        order = Order.get_or_create(user_model.id)
        order.user_finished = True
        bot_cls.sql.protected_commit()

        await state.set_state("submitting_an_order_for_execution")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(
            "Мы получили ваш заказ, ждите сообщения о его готовности. Спасибо, что выбрали нас!"
        )
        await callback_query.answer(
            "Мы получили ваш заказ, ждите сообщения о его готовности. Спасибо, что выбрали нас!",
            show_alert=True
        )


async def kb_new_order(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == 'button_new_order':
        user_model = bot_cls.sql.session.query(Users).filter(Users.tg_id==callback_query.from_user.id).first()
        await callback_query.message.answer(
            f"Рады снова вас видеть, {user_model.full_name}. Прошу, делайте свой заказ.",
            reply_markup=inline_keyboard.kb_menu
        )
        await state.set_state("view_menu")


def register_callback(dp: Dispatcher):
    dp.register_callback_query_handler(button_choose_menu, state="view_menu")
    dp.register_callback_query_handler(kb_main_courses_menu, state="main_courses_menu")
    dp.register_callback_query_handler(kb_bakery_menu, state="bakery_menu")
    dp.register_callback_query_handler(kb_order_menu, state="order_menu")
    dp.register_callback_query_handler(kb_new_order, state="submitting_an_order_for_execution")
