from typing import Any, TypeVar

from sqlalchemy.orm import registry, DeclarativeMeta

from tgbot.models.models import ModelInterface
from tgbot.services.utils import get_clss

mapper_registry = registry()


class BaseModel(ModelInterface, metaclass=DeclarativeMeta):
    __abstract__ = True

    registry = mapper_registry
    metadata = mapper_registry.metadata

    __init__ = mapper_registry.constructor


def init_models(module: Any) -> None:
    clss = get_clss(module)
    for cls in clss:
        if isinstance(cls, type(BaseModel)) and hasattr(cls, 'init'):
            cls.init()


_BM = TypeVar('_BM', bound=BaseModel)