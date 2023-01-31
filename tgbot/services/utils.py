from typing import Any


def get_clss(module: Any):
    return [
        cls
        for name, cls in module.__dict__.items()
        if isinstance(cls, type)
    ]