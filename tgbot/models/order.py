from sqlalchemy import Column, Integer, Unicode, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

from bot_cls import bot_cls
from tgbot.models.base_model import BaseModel


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship(
        'Users',
        uselist=False,
        backref=backref('orders', cascade='all, delete-orphan'),
        foreign_keys=[user_id]
    )

    order_list = Column(Unicode(1024))

    total_price = Column(Integer, nullable=False)

    user_finished = Column(Boolean, default=False)

    Checked = Column(Boolean, default=False)

    @staticmethod
    def get_or_create(user_id: int):
        instance = bot_cls.sql.session.query(Order).filter(Order.user_id == user_id, Order.user_finished==False).first()

        if instance is None:
            instance = Order(
                user_id=user_id,
                order_list='',
                total_price=0
            )
            bot_cls.sql.session.add(instance)
            bot_cls.sql.protected_commit()

        return instance
