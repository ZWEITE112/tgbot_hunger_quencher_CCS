from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_cls import bot_cls
from tgbot.keyboards.inline import inline_keyboard
from tgbot.misc.total_price_counter import total_price_counter
from tgbot.models.order import Order
from tgbot.models.users import Users


async def admin_start(message: Message, state: FSMContext):
    await message.reply("Здраствуйте, администратор!", reply_markup=inline_keyboard.kb_admin)
    await state.set_state('admin_menu')


async def admin_menu(callback_query: types.CallbackQuery, state: FSMContext):
    orders = bot_cls.sql.session.query(Order).filter(Order.Checked == False).all()

    for order in orders:
        order_list = order.order_list.split('|')
        order_string = ''
        for order_item in range(len(order_list)):
            order_string += f"{order_item}. {order_list[order_item]}\n"

        user = bot_cls.sql.session.query(Users).filter(Users.id == order.user_id).first()

        await callback_query.message.answer(
            f'Заказчик: {user.full_name}\n{"="*10}\n'
            f'Заказ:\n{order_string}{"="*10}\n'
            f'{total_price_counter.total_count}'
        )


async def admin_cmd_orders_completed(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('sdfdsfsdfsdf', reply_markup=inline_keyboard.kb_admin_oc)
    orders = bot_cls.sql.session.query(Order).filter(Order.Checked == False).all()

    for order in orders:
        order.Checked = True
        bot_cls.sql.protected_commit()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(admin_menu, state="admin_menu", is_admin=True)
    dp.register_callback_query_handler(admin_cmd_orders_completed, state="admin_menu", is_admin=True)

    # if message.from_user.id == config.tg_bot.admin_ids:
    #     await state.set_state("admin_menu")
    #     await message.answer(f"Здраствуйте, администратор.")
