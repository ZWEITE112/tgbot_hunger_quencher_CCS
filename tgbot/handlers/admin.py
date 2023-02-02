from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.models.order import Order


async def admin_start(message: Message, state: FSMContext):
    await state.set_state("admin_menu")
    await message.reply("Здраствуйте, администратор!", reply_markup=inline_keyboard.kb_admin)


async def admin_menu(callback_query: types.CallbackQuery, state: FSMContext):
    orders = bot_cls.sql.session.query(Order).filter(
        Order.Checked == False,
        Order.user_finished == True
    ).all()

    if orders:
        for order in orders:
            print(order.user_id)
            print(order.user)
            order_list = order.order_list.split('|')
            order_string = ''
            for order_item in range(len(order_list)):
                order_string += f"{order_item+1}. {order_list[order_item]}\n"

            await callback_query.message.answer(
                f'Заказчик: {order.user.full_name}\n{"="*10}\n'
                f'Заказ:\n{order_string}{"="*10}\n'
                f'{order.total_price}руб.'
            )

        await state.set_state("admin_cmd_orders_completed")
        await callback_query.message.edit_reply_markup()
        await callback_query.message.answer(
            "Невыполненные заказы продемонстрированы сверху", reply_markup=inline_keyboard.kb_admin_oc
        )
    else:
        await callback_query.message.answer("В базе отсутствуют незавершённые заказы!")
        await callback_query.answer("В базе отсутствуют незавершённые заказы!", show_alert=True)


async def admin_cmd_orders_completed(callback_query: types.CallbackQuery, state: FSMContext):
    orders = bot_cls.sql.session.query(Order).filter(
        Order.Checked == False,
        Order.user_finished == True
    ).all()

    for order in orders:
        await callback_query.bot.send_message(
            order.user.tg_id,
            "Ваш заказ выполнен, можете его забирать!",
            reply_markup=inline_keyboard.kb_new_order
        )

        order.Checked = True
        bot_cls.sql.protected_commit()

    await callback_query.message.answer("Все заказы выполнены!")
    await callback_query.answer("Все заказы выполнены!", show_alert=True)

    await state.set_state('admin_menu')
    await callback_query.message.answer("Здраствуйте, администратор!", reply_markup=inline_keyboard.kb_admin)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(admin_menu, state="admin_menu", is_admin=True)
    dp.register_callback_query_handler(admin_cmd_orders_completed, state="admin_cmd_orders_completed", is_admin=True)
