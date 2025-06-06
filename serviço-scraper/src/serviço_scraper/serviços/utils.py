from collections.abc import Callable


def implementa(função_implementada: Callable) -> Callable:
    def decorador(func: Callable):
        if func.__doc__ is None:
            func.__doc__ = função_implementada.__doc__

        return func

    return decorador
