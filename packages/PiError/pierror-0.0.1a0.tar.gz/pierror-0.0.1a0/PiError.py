"""A module for allowing Python exceptions to be returned as values."""

from typing import Any, Callable, Optional


class PiError(object):
    """Create a custom error object that can be stored as a value simplifying error propagation.
    This class can also be used as a decorator where the return value type hint of the callable
    must contain the 'PiError' class. Instead of raising an 'Exception', one can instead return a
    'PiError' object containing the exception, which can then be raised later if or when necessary.
    """
    __slots__ = ('expect', 'error', 'cause', 'invalid')

    def __new__(cls: type['PiError'], expect: dict[int, set[type]], error: type, cause: str, /) -> 'PiError':
        """Create and return a new 'PiError' object."""
        assert isinstance(expect, dict), "'expect' must be a 'dict'"
        assert len(expect) >= 0, "length of 'expect' must be >= 0"
        assert type(error) is type, "'error' must be of type 'type'"
        assert isinstance(cause, str), "'cause' must be of type 'str'"
      
        for key, values in expect.items():
            if not isinstance(key, int) and not isinstance(values, set):
                raise TypeError("'keys' must be of type 'int' and 'values' of type 'set'")
            elif isinstance(key, int) and key < 0:
                raise KeyError("The 'key' must be >= 0")
            else:
                match all( [type(t) is type for t in values] ):
                    case True:
                        continue
                    case _:
                        raise TypeError("set items must be of type 'type'")

        if not issubclass(error, (BaseException, Exception)):
            raise AssertionError("The error 'error' must be a subclass of 'BaseException' or 'Exception'")
        else:
            cls.invalid = list()
            return super(PiError, cls).__new__(cls)

    def __init__(self: 'PiError', expect: dict[int, set[type]], error: type, cause: str, /) -> None:
        """Initialize 'PiError' instance attributes."""
        self.expect: dict[int, set[type]] = expect
        self.error: type = error
        self.cause: str = cause

    def __str__(self: 'PiError', /) -> str:
        """Return the instance object as a string."""
        temp_dict = dict()
        for k,v in self.expect.items():
            for item in v:
                temp_dict[k] = item.__name__
        return f'PiError(expect={temp_dict}, error={self.error.__name__!r}, cause={self.cause!r})'

    def __repr__(self: 'PiError', /) -> str:
        """Return a string representation of the instance."""
        return self.__str__()

    def __call__(self: 'PiError', callback: Optional[Callable], /) -> Callable[..., Any] | 'PiError' | None:
        """Allow for decorator functionality, which simplifies error propagation."""

        def decorate(*args) -> Callable[..., Any] | None:
            if callback is None:
                return None
            elif type(callback) is not type and callable(callback):
                assert hasattr(callback, '__annotations__'), f"'__annotations__' attribute not found on '{callback.__name__}'"
                assert 'return' in callback.__annotations__.keys(), f"'return' key not found in '{callback.__name__}.__annotations__'"
                annotation = callback.__annotations__['return']
                assert PiError in annotation.__args__, "'PiError' must be a type hint in the return type annotation"

                if not args:
                    return callback()
                else:
                    assert len(self.expect) == len(args), "'expect' and 'args' must have the same length"
                    for key, values in self.expect.items():
                        arg = args[key]
                        if type(arg) not in values:
                            return self
                        else:
                            continue
                    else:
                        return callback(*args)
            else:
                raise TypeError("The 'callback' must be a 'function / method'")

        return decorate
