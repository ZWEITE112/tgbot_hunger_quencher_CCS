from sqlalchemy import Column, Integer, Unicode

from tgbot.models.base_model import BaseModel


class MainCourse(BaseModel):
    __tablename__ = "main_courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dish_name = Column(Unicode(50), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
