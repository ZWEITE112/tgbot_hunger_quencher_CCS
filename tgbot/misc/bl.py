import json
import os

from bot_cls import bot_cls
from tgbot.models.bakery import Bakery
from tgbot.models.base_model import BaseModel
from tgbot.models.main_courses import MainCourse


def compare_data(json_name: str, model_cls: BaseModel):
    with open(f'static{os.sep}{json_name}', 'r', encoding='utf-8') as fh:
        courses_dict = json.load(fh)

    for course, price in courses_dict.items():
        if bot_cls.sql.session.query(model_cls).filter(
            model_cls.dish_name == course,
            model_cls.price == price
        ).first() is None:
            new_course = model_cls(
                dish_name=course,
                price=price
            )
            bot_cls.sql.session.add(new_course)
            bot_cls.sql.protected_commit()


def check_readiness():
    compare_data('main_courses.json', MainCourse)
    compare_data('bakery.json', Bakery)
