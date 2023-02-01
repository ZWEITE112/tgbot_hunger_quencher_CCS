from sqlalchemy import Column, Integer, Unicode

from tgbot.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False, unique=True)
    full_name = Column(Unicode(50), nullable=False, unique=True)
