from __future__ import annotations

from typing import Any, TYPE_CHECKING, Generic

from sqlalchemy.orm import Query

from tgbot.services import utils


if TYPE_CHECKING:
    from bot_cls import bot_cls
    from base_model import _BM


def init_models(module: Any):
    clss = utils.get_clss(module)
    for cls in clss:
        if hasattr(cls, 'init'):
            cls.init()


class ModelInterface:
    delete_attribute = ('available', False)
    id_attribute = ('id',)

    def __init__(self, **kwargs):
        # Do not use it.
        pass

    @classmethod
    def init(cls):
        pass

    @staticmethod
    def _build_filters(cls, **kwargs) -> list[bool]:
        return [
            getattr(cls, attr) == value for attr, value in kwargs.items()
        ]

    @classmethod
    def get_or_create(cls, **kwargs) -> Generic[_BM]:
        filters = cls._build_filters(cls, **kwargs)

        instance = bot_cls.sql.session.query(cls).filter(*filters).first()

        if instance is None:
            instance = cls.create(cls, **kwargs)

        return instance

    @staticmethod
    def create(cls, **kwargs) -> Generic[_BM]:
        instance = cls(**kwargs)

        bot_cls.sql.session.add(instance)
        bot_cls.sql.protected_commit()

        return instance

    @classmethod
    def schema_to_instance(cls, *args, **kwargs) -> Generic[_BM]:
        pass

    def delete(self):
        if hasattr(self, self.delete_attribute[0]):
            setattr(self, self.delete_attribute[0], self.delete_attribute[1])
        else:
            bot_cls.sql.session.query(type(self)).filter(
                getattr(type(self), self.id_attribute[0])
                == getattr(self, self.id_attribute[0])
            ).delete()

        bot_cls.sql.protected_commit()

    def restore(self) -> None:
        if hasattr(self, self.delete_attribute[0]):
            if (
                getattr(self, self.delete_attribute[0])
                == self.delete_attribute[1]
            ):
                setattr(
                    self, self.delete_attribute[0], not self.delete_attribute[1]
                )
            else:
                raise Exception('Model available so couldn\'t be restored.')
        else:
            raise Exception('Model has not delete field.')

    @classmethod
    def build_query(cls, **kwargs) -> Query:
        filters = cls._build_filters(cls, **kwargs)
        return bot_cls.sql.session.query(cls).filter(**filters)
