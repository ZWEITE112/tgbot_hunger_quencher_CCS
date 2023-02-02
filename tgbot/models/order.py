from sqlalchemy import Column, Integer, Unicode, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from tgbot.models.base_model import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('Users', uselist=False, backref=backref('orders', cascade='all, delete-orphan'))

    order_list = Column(Unicode(1024))

    total_price = Column(Integer, nullable=False)

    Checked = Column(Boolean, default=False)
