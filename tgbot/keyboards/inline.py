from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_cls import bot_cls
from tgbot.models.main_courses import MainCourse
from tgbot.models.bakery import Bakery
from aiogram.utils.callback_data import CallbackData


class InLineKb:
    def __init__(self):
        self.inline_btn_get_orders = InlineKeyboardButton("Получить заказы", callback_data="button_get_orders")
        self.inline_btn_orders_completed = InlineKeyboardButton("Выполнить все заказы",
                                                                callback_data="button_orders_completed")

        self.inline_btn_new_order = InlineKeyboardButton("Новый заказ", callback_data="button_new_order")

        self.inline_btn_main_courses = InlineKeyboardButton("Вторые блюда", callback_data="button_main_courses")
        self.inline_btn_bakery = InlineKeyboardButton("Выпечка", callback_data="button_bakery")

        self.come_back_btn = InlineKeyboardButton("Назад", callback_data="come_back")
        self.inline_btn_ordering = InlineKeyboardButton("Оформление заказа", callback_data="button_ordering")
        self.inline_btn_finish_finish_ordering = InlineKeyboardButton("Закончить оформление заказа",
                                                                      callback_data="button_finish_ordering")

        self.kb_new_order = InlineKeyboardMarkup().add(self.inline_btn_new_order)

        self.kb_admin = InlineKeyboardMarkup().add(self.inline_btn_get_orders)
        self.kb_admin_orders_completed = InlineKeyboardMarkup().add(self.inline_btn_orders_completed)

        self.kb_menu = InlineKeyboardMarkup().row(
            self.inline_btn_main_courses,
            self.inline_btn_bakery).add(self.inline_btn_ordering)

        self._main_courses_btn = None

        self.kb_main_courses_menu = InlineKeyboardMarkup(row_width=1).add(*self.main_courses_btn)
        self.kb_main_courses_menu.add(self.come_back_btn)

        self._bakery_btn = None

        self.kb_bakery_menu = InlineKeyboardMarkup(row_width=1).add(*self.bakery_btn)
        self.kb_bakery_menu.add(self.come_back_btn)

        self.kb_order_menu = InlineKeyboardMarkup(row_width=1).add(
            self.inline_btn_finish_finish_ordering,
            self.come_back_btn
            )

    @property
    def bakery_btn(self):
        if self._bakery_btn is None:
            self._bakery_btn = (
                InlineKeyboardButton(
                    f"{course.dish_name} - {course.price}руб.", callback_data=f"button_bakery{course.id}"
                )
                for course in bot_cls.sql.session.query(Bakery).all()
            )

        return self._bakery_btn

    @property
    def main_courses_btn(self):
        if self._main_courses_btn is None:
            self._main_courses_btn = [
                InlineKeyboardButton(
                    f"{course.dish_name} - {course.price}руб.", callback_data=f"button_main_courses{course.id}"
                )
                for course in bot_cls.sql.session.query(MainCourse).all()
            ]

        return self._main_courses_btn


inline_keyboard = InLineKb()
