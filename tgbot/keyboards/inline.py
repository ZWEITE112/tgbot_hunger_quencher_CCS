from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_cls import bot_cls
from tgbot.models.main_courses import MainCourse
from tgbot.models.bakery import Bakery
from aiogram.utils.callback_data import CallbackData


class InLineKb:
    def __init__(self):
        self.come_back_btn = InlineKeyboardButton("Назад", callback_data="come_back")

        self.inline_btn_mc = InlineKeyboardButton("Вторые блюда", callback_data="button_main_courses")
        self.inline_btn_b = InlineKeyboardButton("Выпечка", callback_data="button_bakery")

        self.inline_btn_op = InlineKeyboardButton("Оформление заказа", callback_data="button_ordering")

        self.kb_menu = InlineKeyboardMarkup().row(self.inline_btn_mc, self.inline_btn_b)
        self.kb_menu_with_o = InlineKeyboardMarkup().row(self.inline_btn_mc, self.inline_btn_b, self.inline_btn_op)

        self.main_courses_btn = [
            InlineKeyboardButton(
                f"{course.dish_name} - {course.price}руб.", callback_data=f"button_main_courses{course.id}"
            )
            for course in bot_cls.sql.session.query(MainCourse).all()
        ]

        self.kb_main_courses_menu = InlineKeyboardMarkup(row_width=1).add(*self.main_courses_btn)

        self.bakery_btn = (
            InlineKeyboardButton(
                f"{course.dish_name} - {course.price}руб.", callback_data=f"button_bakery{course.id}"
            )
            for course in bot_cls.sql.session.query(Bakery).all()
        )

        self.kb_bakery_menu = InlineKeyboardMarkup(row_width=1).add(*self.bakery_btn)

        self.kb_main_courses_menu.add(self.come_back_btn)
        self.kb_bakery_menu.add(self.come_back_btn)


inline_keyboard = InLineKb()
